import pandas as pd

def standardize_column_names(df, column_mapping):
    # Convert all column names to lowercase and strip whitespace
    df.columns = df.columns.str.strip().str.lower()
    
    # Apply the column mapping to rename columns
    standardized_columns = {col: column_mapping.get(col, col) for col in df.columns}
    df.rename(columns=standardized_columns, inplace=True)
    
    # Print the columns after standardization for debugging
    print("Columns after standardization:", df.columns.tolist())

def map_grade_level(grade_level):
    if grade_level.lower() == "0":
        return "K"
    elif grade_level.lower() == "-1":
        return "TK"
    elif grade_level.lower() == "1st grade":
        return "1st Grade"
    elif grade_level.lower() == "grade 1":
        return "Grade 1"
    return grade_level.title() if grade_level.lower() != "tk" else "TK"  # Ensure capitalization for TK

def process_data(test_data, codes, enrolled='', waitlisted=''):
    # Ensure required columns are present in test_data
    required_test_data_columns = ['student id', 'school name', 'grade level', 'enrollment status']
    for col in required_test_data_columns:
        if col not in test_data.columns.str.lower():
            raise KeyError(f"Missing required column in test_data: '{col}'")

    # Ensure required columns are present in codes
    required_codes_columns = ['program code', 'session code', 'program name', 'provider id', 'provider name', 'school id', 'school name']
    
    # Check if 'grade levels' is present in the codes DataFrame
    if 'grade levels' in codes.columns:
        required_codes_columns.append('grade levels')
    
    # Check for missing columns in the codes DataFrame
    for col in required_codes_columns:
        if col not in codes.columns:
            raise KeyError(f"Missing required column in codes: '{col}'")

    output_rows = []
    error_rows = []
    
    for index, row in test_data.iterrows():
        student_id = row.get('student id')
        school_name = row.get('school name')
        grade_level = str(row.get('grade level')).strip() if pd.notna(row.get('grade level')) else None
        enrollment_status = row.get('enrollment status')

        print(f"Processing row {index}:")
        print(f"  Student ID: {student_id}")
        print(f"  School Name: {school_name}")
        print(f"  Grade Level: {grade_level}")
        print(f"  Enrollment Status: {enrollment_status}")

        if grade_level:
            grade_level = map_grade_level(grade_level)
            print(f"  Mapped Grade Level: {grade_level}")

        if pd.isna(student_id) or not str(student_id).isdigit():
            print("  Invalid Student ID")
            error_rows.append(row)
            continue

        if pd.notna(enrollment_status):
            enrollment_status = str(enrollment_status).strip().lower()
        else:
            enrollment_status = ""

        if grade_level:
            # Check if Grade Levels column exists in codes
            if 'grade levels' in codes.columns:
                matching_code = codes[
                    (codes['school name'].str.lower() == school_name.lower()) &
                    (codes['grade levels'].str.lower() == grade_level.lower())
                ]
            else:
                matching_code = codes[
                    (codes['school name'].str.lower() == school_name.lower()) &
                    (codes['program name'].str.lower().str.contains(grade_level.lower(), na=False))
                ]

            if not matching_code.empty:
                school_id = matching_code['school id'].values[0]
                provider_id = matching_code['provider id'].values[0]
                program_code = matching_code['program code'].values[0]
                session_code = matching_code['session code'].values[0]
                
                waitlist_status = ''
                if waitlisted and waitlisted in enrollment_status:
                    waitlist_status = '1'
                elif enrolled and enrolled in enrollment_status:
                    waitlist_status = ''

                output_rows.append({
                    'School ID': school_id,
                    'Provider ID': provider_id,
                    'Program Code': program_code,
                    'Session Code': session_code,
                    'Student ID': student_id,
                    'To Waitlist': waitlist_status
                })
                print("  Row processed successfully")
            else:
                print("  No matching code found")
                error_rows.append(row)
        else:
            print("  Invalid Grade Level")
            error_rows.append(row)

    output_df = pd.DataFrame(output_rows)
    error_df = pd.DataFrame(error_rows)
    return output_df, error_df