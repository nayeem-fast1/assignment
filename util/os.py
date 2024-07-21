import os
import shutil


def delete_files_folders(path):
    """
    Delete the file or directory at the specified path.
    If the path is a directory, all its contents including subdirectories will be deleted.

    Parameters:
    path (str): The file or directory path to delete.
    """
    if os.path.exists(path):
        # If it's a file, delete it
        if os.path.isfile(path):
            os.remove(path)
        # If it's a directory, delete it and all its contents
        elif os.path.isdir(path):
            shutil.rmtree(path)
