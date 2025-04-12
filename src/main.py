import os, shutil

def main():
    copy_static_resources()

def copy_static_resources(src="static", dest="public"):
    """
    Clears the destination directory and recursively copies files
    from the source directory to the destination directory.
    """
    print(f"Preparing to copy from '{src}' to '{dest}'...")
    # Ensure source directory exists
    if not os.path.exists(src):
        raise ValueError(f"Source directory '{src}' does not exist.")
    if not os.path.isdir(src):
         raise ValueError(f"Source '{src}' is not a directory.")

    # Remove existing destination directory/file
    if os.path.exists(dest):
        print(f"Removing existing destination: '{dest}'")
        # Check if it's a directory before using rmtree
        if os.path.isdir(dest):
             shutil.rmtree(dest)
        else:
             os.remove(dest)

    # Create the top-level destination directory
    print(f"Creating destination directory: '{dest}'")
    # Use makedirs for safety, though mkdir would likely work here
    os.makedirs(dest, exist_ok=True)

    # Start the recursive copy process
    recursive_copy(src, dest)
    print("Copy complete.")


def recursive_copy(src_dir, dest_dir):
    """
    Recursively copies contents from src_dir to dest_dir.
    Assumes src_dir exists and dest_dir exists.
    """
    print(f"Processing source: {src_dir} -> Dest: {dest_dir}") # Debug print
    for item in os.listdir(src_dir):
        # Construct full source and destination paths using os.path.join
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        # Check if the current item is a directory
        if os.path.isdir(src_path):
            # Create the corresponding directory in the destination
            # Use exist_ok=True in case it somehow already exists (though unlikely with rmtree)
            print(f"  Creating directory: {dest_path}") # Debug print
            os.makedirs(dest_path, exist_ok=True)
            # Recursively call copy for the subdirectory
            recursive_copy(src_path, dest_path)
        # Check if the current item is a file
        elif os.path.isfile(src_path):
            # Copy the file
            print(f"  Copying file: {src_path} -> {dest_path}") # Debug print
            shutil.copy2(src_path, dest_path) # copy2 preserves more metadata than copy
        else:
            # Optionally handle other types like symbolic links, or just ignore them
            print(f"  Skipping item (not file or directory): {src_path}")

if __name__ == "__main__":
    main()