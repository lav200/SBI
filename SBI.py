import pandas as pd
import sweetviz as sv
from pandas_profiling import ProfileReport
import streamlit as st

def process_file(uploaded_file):
    try:
        # Attempt to read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please use .csv or .xlsx files.")

        st.write("Data loaded successfully!")

        # Display basic information about the dataset
        st.write("Dataset Info:")
        st.write(df.info())
        st.write("\nDataset Head:")
        st.write(df.head())

        # Remove duplicate rows
        initial_rows = df.shape[0]
        df = df.drop_duplicates()
        final_rows = df.shape[0]
        st.write(f"Removed {initial_rows - final_rows} duplicate rows.")

        # Handle missing values (example: fill with median for numeric columns and mode for categorical columns)
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0], inplace=True)

        st.write("Missing values handled.")

        # Handle mixed-type columns
        mixed_type_columns = []
        for col in df.columns:
            if pd.api.types.infer_dtype(df[col]) == "mixed":
                mixed_type_columns.append(col)
                st.write(f"Column {col} has mixed types. Converting to strings for consistency.")
                df[col] = df[col].astype(str)

        # Save the cleaned data
        cleaned_file_path = 'cleaned_data.csv'
        df.to_csv(cleaned_file_path, index=False)
        st.write(f"Cleaned data saved to {cleaned_file_path}.")

        # Generate Sweetviz report
        sweetviz_report = sv.analyze(df)
        sweetviz_report_file = "sweetviz_report.html"
        sweetviz_report.show_html(sweetviz_report_file)
        st.write(f"Sweetviz report generated: [Download Sweetviz Report](./{sweetviz_report_file})")

        # Generate Pandas Profiling report
        pandas_profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
        pandas_profile_file = "pandas_profiling_report.html"
        pandas_profile.to_file(pandas_profile_file)
        st.write(f"Pandas profiling report generated: [Download Pandas Profiling Report](./{pandas_profile_file})")

    except Exception as e:
        st.write(f"An error occurred: {e}")

# Streamlit app
st.title("Data Analysis Tool")

st.write("Upload your dataset (.csv or .xlsx) to begin analysis:")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    process_file(uploaded_file)
