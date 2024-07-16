import os
import shutil
from page_generator import generate_pages_recursive

# Get the absolute path of the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {destination_path}")
        else:
            copy_directory(source_path, destination_path)
            print(f"Copied directory: {destination_path}")

def main():
    # Define paths
    content_dir = os.path.join(PROJECT_ROOT, "content")
    static_dir = os.path.join(PROJECT_ROOT, "static")
    public_dir = os.path.join(PROJECT_ROOT, "public")
    template_path = os.path.join(PROJECT_ROOT, "template.html")

    # Delete and recreate public directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

    # Copy static files
    copy_directory(static_dir, public_dir)

    # Generate pages recursively
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()