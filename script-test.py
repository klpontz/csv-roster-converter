import unittest
import pandas as pd
from io import StringIO
from processing_module import process_data, map_grade_level, standardize_column_names

class TestProcessingScript(unittest.TestCase):

    def setUp(self):
        self.test_data_csv = StringIO("""Student ID,Grade Level,Enrollment Status,School Name
2041751,1st grade,enrolled,Buena Vista Elementary
2040798,grade 1,waitlisted,Buena Vista Elementary
2101439,TK,enrolled,Buena Vista Elementary
2040094,K,enrolled,Buena Vista Elementary
""")
        
        self.codes_csv = StringIO("""program_code,session_code,prog_name,provider_id,provider_name,school_id,sch_name,grade_levels
appm-67dv-282c,Buena vista2,Afterschool Child Care - 1st Grade,4951,YMCA at Lompoc USD,10563,Buena Vista Elementary,1st Grade
8mmg-sd43-yxg9,Buena vistak,Afterschool Child Care - K,4951,YMCA at Lompoc USD,10563,Buena Vista Elementary,K
7zp2-hj9a-7s6q,Buena vista1,Afterschool Child Care 1st Grade,4951,YMCA at Lompoc USD,10563,Buena Vista Elementary,Grade 1
appm-67dv-282c,Buena vista2,Afterschool Child Care - Grade 1,4951,YMCA at Lompoc USD,10563,Buena Vista Elementary,Grade 1
""")

        # Load into DataFrames
        self.test_data = pd.read_csv(self.test_data_csv)
        self.codes = pd.read_csv(self.codes_csv)

        # Standardize column names
        standardize_column_names(self.test_data, {'student id': 'Student ID', 'grade': 'Grade Level', 'waitlist': 'Enrollment Status', 'school': 'School Name'})
        standardize_column_names(self.codes, {'program_code': 'Program Code', 'session_code': 'Session Code', 'prog_name': 'Program Name', 'provider_id': 'Provider ID', 'provider_name': 'Provider Name', 'school_id': 'School ID', 'sch_name': 'School Name', 'grade_levels': 'Grade Levels'})

    def test_processing_with_grade_levels_column(self):
        processed_output, errors = process_data(self.test_data, self.codes)
        self.assertEqual(len(errors), 1)  # Expect exactly 1 error row due to missing code for TK
        self.assertEqual(len(processed_output), 3)  # The other 3 rows should be processed correctly

    def test_map_grade_level(self):
        self.assertEqual(map_grade_level("1st grade"), "1st Grade")
        self.assertEqual(map_grade_level("grade 1"), "Grade 1")
        self.assertEqual(map_grade_level("K"), "K")
        self.assertEqual(map_grade_level("TK"), "TK")

    def test_grade_level_variants(self):
        grade_level = "1st grade"
        self.assertIn(map_grade_level(grade_level), ['1st Grade', 'Grade 1', 'K', 'TK'])

    def test_non_numeric_student_id(self):
        self.test_data.loc[0, 'Student ID'] = "ABC123"
        processed_output, errors = process_data(self.test_data, self.codes)
        self.assertEqual(len(errors), 2)  # Expect exactly 2 error rows (1 for non-numeric ID, 1 for missing code)

    def test_processing_with_explicit_grade_level_column(self):
        processed_output, errors = process_data(self.test_data, self.codes)
        self.assertEqual(len(errors), 1)  # Expect exactly 1 error row due to missing code for TK

    def test_empty_user_input(self):
        enrolled = ''
        waitlisted = ''
        processed_output, errors = process_data(self.test_data, self.codes, enrolled=enrolled, waitlisted=waitlisted)
        self.assertEqual(len(errors), 1)  # Expect 1 error due to missing code for TK

    def test_missing_columns_in_test_data(self):
        # Ensure the column exists before dropping
        if 'grade level' in self.test_data.columns:
            self.test_data.drop(columns=['grade level'], inplace=True)
        with self.assertRaises(KeyError):
            process_data(self.test_data, self.codes)

    def test_missing_columns_in_codes(self):
        # Remove 'Program Name' column
        self.codes.drop(columns=['Program Name'], inplace=True)
        with self.assertRaises(KeyError):
            process_data(self.test_data, self.codes)      

    def test_additional_unmapped_grade_levels(self):
        # Add a row with an unmapped grade level (e.g., "2nd grade")
        new_row = pd.DataFrame({
            'Student ID': ['2040095'], 
            'Grade Level': ['2nd grade'], 
            'Enrollment Status': ['enrolled'], 
            'School Name': ['Buena Vista Elementary']
        })
    
        self.test_data = pd.concat([self.test_data, new_row], ignore_index=True)
    
        processed_output, errors = process_data(self.test_data, self.codes)
        self.assertEqual(len(errors), 2)  # Expect errors for 'TK' and '2nd grade'

    def test_case_insensitivity_in_matching(self):
        # Use the correct standardized column name
        self.test_data['school name'] = self.test_data['school name'].str.upper()
        processed_output, errors = process_data(self.test_data, self.codes)
        self.assertEqual(len(errors), 1)  # Expect 1 error due to 'TK'
        self.assertEqual(len(processed_output), 3)  # Other rows should process successfully

    def test_handling_of_empty_rows(self):
        # Add an empty row
        empty_row = pd.Series([None, None, None, None], index=self.test_data.columns)
        self.test_data = pd.concat([self.test_data, pd.DataFrame([empty_row])], ignore_index=True)
        
        processed_output, errors = process_data(self.test_data, self.codes)
        self.assertEqual(len(errors), 2)  # Expect errors for 'TK' and the empty row

    def test_multiple_matching_codes(self):
        # Duplicate a row in codes to create multiple matches
        duplicate_row = self.codes.iloc[0:1]
        self.codes = pd.concat([self.codes, duplicate_row], ignore_index=True)
        processed_output, errors = process_data(self.test_data, self.codes)
        self.assertEqual(len(errors), 1)  # Expect 1 error due to 'TK'
        self.assertEqual(len(processed_output), 3)  # Other rows should process successfully

    def test_varied_enrollment_status_values(self):
        self.test_data['Enrollment Status'] = ['Enrolled ', ' Waitlisted', 'ENROLLED', 'WAITLISTED']
        processed_output, errors = process_data(self.test_data, self.codes, enrolled='enrolled', waitlisted='waitlisted')
        self.assertEqual(len(errors), 1)  # Expect 1 error for 'TK'
        self.assertEqual(len(processed_output), 3)

if __name__ == '__main__':
    unittest.main()