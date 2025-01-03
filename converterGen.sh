#!/bin/bash

# Find the Python executable location
PYTHON_PATH=$(which python3 || which python)
if [ -z "$PYTHON_PATH" ]; then
    echo "Python is not installed on this system."
    exit 1
fi

# Install the docx2pdf dependency
$PYTHON_PATH -m pip install docx2pdf

# Add shebang to the Python script
SCRIPT_NAME="doc2pdf"
cat <<EOL > $SCRIPT_NAME
#!$PYTHON_PATH
import os
from docx2pdf import convert

def convert_docs_to_pdfs():
    # Create a directory to save converted PDFs if it doesn't exist
    output_dir = './converted_pdfs'
    os.makedirs(output_dir, exist_ok=True)

    # Get all .docx files in the current directory
    current_dir = os.getcwd()
    docx_files = [file for file in os.listdir(current_dir) if file.endswith('.docx')]

    # Convert each .docx file to PDF and save it in the output directory
    for docx_file in docx_files:
        input_path = os.path.join(current_dir, docx_file)
        output_path = os.path.join(output_dir, f'\${os.path.splitext(docx_file)[0]}.pdf')
        convert(input_path, output_path)

    print(f'Converted \${len(docx_files)} files to PDFs and saved them in \${output_dir}.')

if __name__ == '__main__':
    convert_docs_to_pdfs()
EOL

# Make the script executable
chmod +x $SCRIPT_NAME

# Find the first writable directory in the PATH variable
SAVE_PATH=""
IFS=':' read -ra ADDR <<< "$PATH"
for DIR in "${ADDR[@]}"; do
    if [ -w "$DIR" ]; then
        SAVE_PATH="$DIR"
        break
    fi
done

# Move the script to the first writable directory in the PATH variable
if [ -n "$SAVE_PATH" ]; then
    mv $SCRIPT_NAME $SAVE_PATH/
    echo "The script has been moved to $SAVE_PATH and is now executable."
    echo "Now run command "$SCRIPT_NAME" to convert all word files to pdf from current directory."
else
    echo "No writable directory found in the PATH variable."
    exit 1
fi
