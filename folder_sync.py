import os
import shutil
import sys
import time
import logging
import argparse


def logger_setup(
    log_path: str
) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path)
        ]
    )


def create_directory_if_not_exists(
    directory: str
) -> None:
    # Create the replica folder if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Folder created: {directory}")


def copy_files(
    source_file: str,
    replica_file: str
) -> None:
    # Get the modification times of the source and replica files
    source_mod_time = os.path.getmtime(source_file)
    replica_mod_time = (
        os.path.getmtime(replica_file) if os.path.exists(replica_file) else 0
    )
    if not os.path.exists(replica_file):
        # Copy any missing files in the replica folder from the source folder
        shutil.copy2(source_file, replica_file)
        logging.info(f"File copied: {source_file} -> {replica_file}")
    elif source_mod_time > replica_mod_time:
        # Update the replica file if the source file was changed
        shutil.copy2(source_file, replica_file)
        logging.info(f"File updated: {source_file} -> {replica_file}")


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


def remove_directory_if_not_exists(
    source_folder: str,
    replica_folder: str
) -> None:
    # Remove any replica subfolder if it doesn't exist in source_folder anymore
    if not os.path.exists(source_folder):
        logging.info(f"Removing folder: {replica_folder}")

        # Logs the content of the folder to be removed
        for file in os.listdir(replica_folder):
            logging.info(f"Files in {replica_folder}: {file}")
        shutil.rmtree(replica_folder)
        logging.info(f"Folder removed: {replica_folder}")


def remove_files(
    replica_file: str,
    source_file: str
) -> None:
    # Remove files in replica folder that don't exist in source folder
    if not os.path.exists(source_file):
        os.remove(replica_file)
        logging.info(f"File removed: {replica_file}")


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


def synchronize_folders(
    source_folder: str,
    replica_folder: str
) -> None:
    try:
        create_directory_if_not_exists(replica_folder)
        copy_subfolders_and_files(source_folder, replica_folder)
        remove_subfolders_and_files(source_folder, replica_folder)
    except Exception as e:
        logging.error(f"Synchronization failed: {e}")


if __name__ == "__main__":
    # Example: python3 folder_sync.py src_folder rep_folder 5 events.log
    parser = argparse.ArgumentParser(
        description='Folder synchronization script'
    )
    parser.add_argument(
        'source_folder', type=str, help='Path to the source folder'
    )
    parser.add_argument(
        'replica_folder', type=str, help='Path to the replica folder'
    )
    parser.add_argument(
        'interval', type=int, help='Synchronization interval in seconds'
    )
    parser.add_argument(
        'log_file', type=str, help='Path to the log file'
    )
    args = parser.parse_args()

    source_folder = args.source_folder
    replica_folder = args.replica_folder
    interval = args.interval
    log_file = args.log_file

    logger_setup(log_file)
    logging.info(
        f"Folder synchronization started: {source_folder} -> {replica_folder}"
    )

    try:
        while True:
            synchronize_folders(source_folder, replica_folder)
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Execution interrupted via CTRL-C")
