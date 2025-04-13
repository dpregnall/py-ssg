import os, shutil

from parse import markdown_to_html_node, extract_title

def main():
    copy_static_resources()
    generate_pages_recursive("content", "template.html", "public")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Source directory '{dir_path_content}' does not exist.")
    if not os.path.isdir(dir_path_content):
         raise ValueError(f"Source '{dir_path_content}' is not a directory.")
    
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item.replace(".md",".html"))

        if os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_path)
        elif os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path)
        else:
            print(f"  Skipping item (not file or directory): {src_path}")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    
    print("Extracting source markdown content...")
    with open(from_path) as f:
        source_md = f.read()
    
    print("Extracting html template...")
    with open(template_path) as f:
        template_html = f.read()

    print("Converting source markdown to html...")
    html_content = markdown_to_html_node(source_md).to_html()

    print("Extracting page title from source markdown...")
    html_title = extract_title(source_md)

    print("Populating template with content...")
    html = template_html.replace("{{ Title }}", html_title)
    html = html.replace("{{ Content }}", html_content)

    target_dir = os.path.dirname(dest_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(dest_path, 'w') as f:
        f.write(html)
        f.close()

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