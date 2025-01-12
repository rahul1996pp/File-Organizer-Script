# File Organizer Script

This Python script helps organize files within a directory by categorizing them based on file extensions and size. It moves the files into subfolders grouped by their extension and file size range. The script also generates a metadata JSON file that contains information about the files, including their size and extension.

## Features

- **File Categorization**: The script categorizes files by their extension and size.
- **Size Ranges**: Files are grouped into different size ranges, from small (less than 1 KB) to large (over 10 GB).
- **Parallel Processing**: The script uses concurrent execution to move files efficiently, taking advantage of multiple CPU cores.
- **Metadata Generation**: A JSON file (`file_metadata.json`) is created to store information about the files, including their paths, extensions, and sizes.

## Size Ranges

Files are grouped into the following size ranges:
- 0 to 1 KB
- 1 to 5 KB
- 5 to 10 KB
- 10 to 50 KB
- 50 to 100 KB
- 100 to 500 KB
- 500 to 1000 KB
- 1 to 5 MB
- 5 to 10 MB
- 10 to 50 MB
- 50 to 100 MB
- 100 to 500 MB
- 500 to 1000 MB
- 1 to 5 GB
- 5 to 10 GB
- Greater than 10 GB

## Requirements

- Python 3.x
- `os`, `shutil`, `json`, `multiprocessing`, and `concurrent.futures` modules (standard Python libraries, no installation required)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/rahul1996pp/File-Organizer-Script.git
   ```

2. Navigate to the project folder:
   ```bash
   cd File-Organizer-Script
   ```

3. Ensure you have Python 3.x installed.

## Usage

1. Open a terminal and navigate to the folder containing the script.
2. Run the script:
   ```bash
   python organize_files.py
   ```
3. The script will prompt you to enter the directory you want to organize. Enter the absolute or relative path of the directory. For example:
   ```bash
   Enter the directory to organize: /path/to/directory
   ```

4. The script will:
   - Generate a `file_metadata.json` file containing information about the files.
   - Organize the files into subdirectories based on their file extension and size.
   - Create new folders for each file extension and size category.

## Example Folder Structure

After running the script, your directory may look like this:
```
/path/to/directory/
├── file_metadata.json
├── .txt/
│   ├── 0_to_1_KB/
│   ├── 1_to_5_KB/
│   ├── 5_to_10_KB/
│   └── ...
├── .jpg/
│   ├── 0_to_1_KB/
│   ├── 1_to_5_KB/
│   ├── 5_to_10_KB/
│   └── ...
├── no_extension/
│   ├── 0_to_1_KB/
│   ├── 1_to_5_KB/
│   ├── 5_to_10_KB/
│   └── ...
└── ...
```

## Notes

- Hidden files and directories (those starting with `.`) are ignored during the processing.
- Files that cannot be processed (due to permission issues, for example) will be skipped with an error message.
- The script moves files into the appropriate subfolders. Ensure that you have backups if needed before running the script.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
