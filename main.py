# Prompt for Filename
def input_filename(files):
    file_handles = {}
    for item in files:
        while True:
            handle = input(f'Enter the file name of the {item}: ')
            try:
                with open(handle, 'r') as open_file:
                    print(f'file opened: {handle}')
                    file_handles[item] = open_file.read()
                break  # Break the inner loop once the file is successfully read
            except FileNotFoundError:
                print(f'File {handle} cannot be opened. Try again.')
            except Exception as e:
                print(f'An unexpected error occurred: {e}')
                break  # Optionally break the loop on other exceptions to prevent infinite looping
    return file_handles