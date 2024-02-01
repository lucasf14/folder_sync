
import logging
import os
import shutil
from file_operations import copy_files, remove_files


def create_directory_if_not_exists(
    directory: str
) -> None:
    # Create the replica folder if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Folder created: {directory}")


def remove_directory_if_not_exists(
    source_folder: str,
    replica_folder: str
) -> None:
    # Remove any replica subfolder if it doesn't exist in source_folder anymore
    if not os.path.exists(source_folder):
        for root, dirs, files in os.walk(replica_folder, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                logging.info(f"File removed: {file_path}")

            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
                logging.info(f"Folder removed: {dir_path}")

        shutil.rmtree(replica_folder)
        logging.info(f"Folder removed: {replica_folder}")


def copy_subfolders_and_files(
    source_folder: str,
    replica_folder: str
) -> None:
    # Copy any missing folders and files
    # in the replica folder from the source folder
    for root, dirs, files in os.walk(source_folder):
        for folder in dirs:
            source_subfolder = os.path.join(root, folder)
            replica_subfolder = os.path.join(
                replica_folder,
                os.path.relpath(source_subfolder, source_folder)
            )
            create_directory_if_not_exists(
                replica_subfolder
            )

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(
                replica_folder,
                os.path.relpath(source_file, source_folder)
            )
            copy_files(
                source_file,
                replica_file
            )


def remove_subfolders_and_files(
    source_folder: str,
    replica_folder: str
) -> None:
    # Remove any extra folders or files the replica folder
    for root, dirs, files in os.walk(replica_folder):
        for folder in dirs:
            replica_subfolder = os.path.join(root, folder)
            source_subfolder = os.path.join(
                source_folder,
                os.path.relpath(replica_subfolder, replica_folder)
            )
            remove_directory_if_not_exists(
                source_subfolder,
                replica_subfolder
            )

        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(
                source_folder,
                os.path.relpath(replica_file, replica_folder)
            )
            remove_files(
                replica_file,
                source_file
            )
