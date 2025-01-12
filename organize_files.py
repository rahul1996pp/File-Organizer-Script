import multiprocessing
import os
import shutil
import json
import concurrent.futures
from collections import defaultdict

def create_folder_if_not_exists(folder_path, created_folders):
    """Create a folder if it does not exist, tracking created folders."""
    if folder_path not in created_folders:
        os.makedirs(folder_path, exist_ok=True)
        created_folders.add(folder_path)

def get_size_range_folder(size_in_kb):
    """Determine the folder name based on file size in KB."""
    size_ranges = [
        (0, 1, "0_to_1_KB"), (1, 5, "1_to_5_KB"), (5, 10, "5_to_10_KB"),
        (10, 50, "10_to_50_KB"), (50, 100, "50_to_100_KB"), (100, 500, "100_to_500_KB"),
        (500, 1000, "500_to_1000_KB"), (1000, 5000, "1_to_5_MB"), (5000, 10000, "5_to_10_MB"),
        (10000, 50000, "10_to_50_MB"), (50000, 100000, "50_to_100_MB"), (100000, 500000, "100_to_500_MB"),
        (500000, 1000000, "500_to_1000_MB"), (1000000, 5000000, "1_to_5_GB"), (5000000, 10000000, "5_to_10_GB"),
        (10000000, float("inf"), "greater_than_10_GB")
    ]
    for min_size, max_size, folder_name in size_ranges:
        if min_size < size_in_kb <= max_size:
            return folder_name
    return "unknown_size_range"

def save_file_metadata(base_directory, json_path):
    """Create a JSON file containing metadata of files grouped by extension and size category."""
    file_metadata = defaultdict(lambda: defaultdict(list))

    try:
        for root, _, files in os.walk(base_directory):
            for file in files:
                file_path = os.path.join(root, file)
                if not os.path.isfile(file_path) or file.startswith('.'):  # Skip directories and hidden files
                    continue

                try:
                    size_in_kb = os.path.getsize(file_path) / 1024  # File size in KB
                    extension = os.path.splitext(file)[1].lower()  # File extension
                    size_category = get_size_range_folder(size_in_kb)  # Size category

                    file_metadata[extension][size_category].append({
                        "path": file_path,
                        "size_kb": size_in_kb
                    })
                except OSError as e:
                    print(f"Error processing file {file_path}: {e}")

        with open(json_path, "w") as json_file:
            json.dump(file_metadata, json_file, indent=4)

        print(f"Metadata saved to {json_path}")
    except Exception as e:
        print(f"Error saving metadata: {e}")

def move_file(file_info, size_category_folder):
    """Move a single file to its respective category folder."""
    file_path = file_info["path"]
    target_path = os.path.join(size_category_folder, os.path.basename(file_path))
    try:
        os.rename(file_path, target_path)  # Faster than shutil.move within the same filesystem
        print(f"Moved: {file_path} to {target_path}")
    except OSError as e:
        print(f"Error moving file {file_path}: {e}")

def move_files(file_metadata, base_directory):
    """Move files based on their metadata, with parallel processing."""
    created_folders = set()
    max_workers = multiprocessing.cpu_count()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for extension, size_categories in file_metadata.items():
                extension_folder = os.path.join(base_directory, extension[1:] if extension else "no_extension")
                create_folder_if_not_exists(extension_folder, created_folders)

                for size_category, files in size_categories.items():
                    size_category_folder = os.path.join(extension_folder, size_category)
                    create_folder_if_not_exists(size_category_folder, created_folders)

                    for file_info in files:
                        futures.append(executor.submit(move_file, file_info, size_category_folder))

            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                pass

        print("File classification complete.")
    except Exception as e:
        print(f"Error during file movement: {e}")

if __name__ == "__main__":
    base_directory = input("Enter the directory to organize: ").strip()
    if os.path.isdir(base_directory):
        try:
            json_path = os.path.join(base_directory, "file_metadata.json")
            save_file_metadata(base_directory, json_path)
            with open(json_path, "r") as json_file:
                file_metadata = json.load(json_file)
            move_files(file_metadata, base_directory)
            print("File organization complete.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("The specified directory does not exist or is not a directory.")
