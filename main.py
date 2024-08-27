import pandas as pd
import datetime
from processing_module import process_data, standardize_column_names, map_grade_level

# Prompt for district name
district_name = input("Please enter the district name: ").strip().replace(" ", "_")

# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Load the CSV files
test_data = pd.read_csv('/Users/pontz/Projects/csv-bulk/test-data.csv')
codes = pd.read_csv('/Users/pontz/Projects/csv-bulk/codes.csv')

# Define the column mappings
test_data_mapping = {
    "student id": "Student ID",
    "grade": "Grade Level",
    "waitlist": "Enrollment Status",
    "school": "School Name"
}

codes_mapping = {
    "program_code": "Program Code",
    "session_code": "Session Code",
    "prog_name": "Program Name",
    "provider_id": "Provider ID",
    "provider_name": "Provider Name",
    "school_id": "School ID",
    "sch_name": "School Name"
}

# Standardize column names in both dataframes
standardize_column_names(test_data, test_data_mapping)
standardize_column_names(codes, codes_mapping)

# Prompt user for waitlist mapping
enrolled = input("What should be considered enrolled in a course? (this will map to blank): ").strip().lower()
waitlisted = input("What should be considered a waitlisted student? (this will map to 1): ").strip().lower()

# Process the data
output_df, error_df = process_data(test_data, codes, enrolled, waitlisted)

# Sort the output DataFrame by School ID, Program Code, and Session Code
output_df.sort_values(by=['School ID', 'Program Code', 'Session Code'], inplace=True)

# Define output file names
output_file_name = f"{district_name}-{current_date}-to-upload.csv"
error_file_name = f"{district_name}-{current_date}-error-file.csv"

# Save the output to to_upload.csv
output_df.to_csv(f'/Users/pontz/Projects/csv-bulk/data/{output_file_name}', index=False)

# Save errors to error_file.csv
error_df.to_csv(f'/Users/pontz/Projects/csv-bulk/data/{error_file_name}', index=False)

print(f"Processing complete. Check {output_file_name} for the output and {error_file_name} for any issues.")