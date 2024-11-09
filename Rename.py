import sys
from pathlib import Path
import re

def rename_files(
    folder_path: str,
    new_name: str,
    dry_run: bool = False
) -> tuple[int, list[str]]:
    """
    Rename all files in a directory with sequential volume numbers.
    
    Args:
        folder_path: Path to the directory containing files
        new_name: New base name for the files
        dry_run: If True, only show what would be renamed without actual renaming
    
    Returns:
        tuple containing count of renamed files and list of error messages
    
    Raises:
        FileNotFoundError: If the specified directory doesn't exist
        PermissionError: If lacking permissions to rename files
    """
    folder_path = Path(folder_path)
    if not folder_path.is_dir():
        raise FileNotFoundError(f"Directory not found: {folder_path}")
    
    renamed_count = 0
    errors = []
    regex = r"\d{2}"
    i = 1

    # Get all files and sort them.
    files = [f for f in folder_path.iterdir() if f.is_file()]
    files.sort()
   
    for file_path in files:
        # Check if the filename matches the regex
        match = re.findall(regex, str(file_path))

        if match:
            try:
                new_filename = f"{new_name} vol{match[0]}{file_path.suffix}"
                new_path = folder_path / new_filename

                if not dry_run:
                    file_path.rename(new_path)
                    print(f"Renamed: {file_path.name} → {new_filename}")
                else:
                    print(f"Would rename: {file_path.name} → {new_filename}")
                renamed_count += 1

            except PermissionError:
                errors.append(f"Permission denied: {file_path}")
            except Exception as e:
                errors.append(f"Error processing {file_path}: {str(e)}")

        else:
            try:
                new_filename = f"{new_name} vol{i:02}{file_path.suffix}"
                new_path = folder_path / new_filename

            # Check if target file already exists
                if new_path.exists() and file_path != new_path:
                    errors.append(f"Cannot rename: {new_filename} already exists")

                if not dry_run:
                    file_path.rename(new_path)
                    print(f"Renamed: {file_path.name} → {new_filename}")
                else:
                    print(f"Would rename: {file_path.name} → {new_filename}")
                
                renamed_count += 1

            except PermissionError:
                errors.append(f"Permission denied: {file_path}")
            except Exception as e:
                errors.append(f"Error processing {file_path}: {str(e)}")

    return renamed_count, errors

def parse_args():
    """Parse and validate command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Rename all files in a directory with sequential volume numbers"
    )
    parser.add_argument("folder_path", help="Directory containing files to rename")
    parser.add_argument("new_name", help="New base name for files")
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Show what would be renamed without making changes"
    )
    
    return parser.parse_args()


def main():
    """Main entry point of the script."""
    try:
        args = parse_args()

        count, errors = rename_files(
            args.folder_path,
            args.new_name,
            args.dry_run
        )

        # Print summary
        print(f"\nSummary:")
        print(f"Files processed: {count}")
        if errors:
            print("\nErrors encountered:")
            for error in errors:
                print(f"- {error}")
            return 1
        return 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
