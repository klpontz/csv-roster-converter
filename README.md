# CSV Processing Script

## Overview

This script processes student enrollment data by matching it with program codes provided in another CSV file. The script ensures that each student's data is correctly mapped to the relevant program and generates output and error files based on the processing results.

## Requirements

- Python 3.x
- Pandas library

## Installation

1. Clone the repository or download the script files.
2. Ensure you have Python 3 installed on your system.
3. Install the required Python packages using pip:
   ```bash
   pip install pandas
   ```

## Usage

1. Prepare your input CSV files:
   - `test_data.csv`: Contains student enrollment data.
   - `codes.csv`: Contains program codes and corresponding school information.

2. Run the script using Python:
   ```bash
   python main.py
   ```

3. The script will prompt you for the district name, the enrolled status mapping, and the waitlisted status mapping.

4. After processing, the script will generate two output files:
   - `<district_name>-<date>-to-upload.csv`: Contains the successfully processed data.
   - `<district_name>-<date>-error-file.csv`: Contains rows that couldn't be processed due to errors such as missing or invalid data.

## File Formats

### test_data.csv

This file should contain the following columns:

- `Student ID`: Unique identifier for each student (numeric values).
- `Grade Level`: The student's grade level (e.g., "1st grade", "K", "TK").
- `Enrollment Status`: The student's enrollment status (e.g., "enrolled", "waitlisted").
- `School Name`: The name of the school the student is enrolled in.

### codes.csv

This file should contain the following columns:

- `Program Code`: Unique identifier for the program.
- `Session Code`: Unique identifier for the session.
- `Program Name`: The name of the program.
- `Provider ID`: Unique identifier for the provider.
- `Provider Name`: The name of the provider.
- `School ID`: Unique identifier for the school.
- `School Name`: The name of the school.
- `Grade Levels` (optional): The grade levels associated with the program.

### Example

Example `test_data.csv`:

```csv
Student ID,Grade Level,Enrollment Status,School Name
0000011,1st grade,enrolled,BV Elementary
1100001,grade 1,waitlisted,BV Elementary
1010101,TK,enrolled,BV Elementary
1111101,K,enrolled,BV Elementary
```

Example `codes.csv`:

```csv
Program Code,Session Code,Program Name,Provider ID,Provider Name,School ID,School Name,Grade Levels
appm-67dv-282c,Bvista2,Afterschool Child Care - 1st Grade,4951,YMCA USD,10563,Buena Vista Elementary,1st grade
8mmg-sd43-yxg9,Bk,Afterschool Child Care - K,4951,YMCA USD,10563,Buena Vista Elementary,K
7zp2-hj9a-7s6q,Bista1,Afterschool Child Care 1st Grade,4951,YMCA USD,10563,Buena Vista Elementary,1st grade
```

## Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest script-test.py
```

The tests will validate the processing logic, including handling of various edge cases such as missing columns, case insensitivity, and more.

## Contributing

If you'd like to contribute to this project, feel free to open a pull request or submit an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
