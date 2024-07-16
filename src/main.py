import os
import shutil

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

source_directory = "/Users/izelniyage/Documents/boot.dev/staticsitegen/static"
destination_directory = "/Users/izelniyage/Documents/boot.dev/staticsitegen/public"

if __name__ == "__main__":
    copy_directory(source_directory, destination_directory)

