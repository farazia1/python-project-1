import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for white text
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, rgb(77, 24, 190), rgba(117, 103, 212, 0.67), rgba(57, 204, 50, 0.95));
        color: white;
    }
    .custom-text {
        color: white !important;
        font-weight: bold;
    }
    .stFileUploader label {
        color: white !important;
        font-weight: bold;
    }
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        color: white !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Description
st.title("Data Sweeper")
st.write("This is a simple data sweeper app")

# File Uploader
st.markdown('<p class="custom-text">Upload your files (CSV or Excel only):</p>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=["csv", "xlsx"], accept_multiple_files=True)

if not uploaded_files:
    st.markdown('<p class="stAlert">⚠ Please upload at least one CSV or Excel file.</p>', unsafe_allow_html=True)
else:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            continue

        # Display Data Preview
        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader(f"Cleaning Options for {file.name}")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed successfully!")

            with col2:
                if st.button(f"Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled with column mean!")

        # Column Selection
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to", ["csv", "excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type.upper()}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    # ✅ Success message with white text
    st.markdown('<p class="stAlert">✅ All files processed successfully!</p>', unsafe_allow_html=True)
