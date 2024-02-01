import time
import logging
import argparse
from logger import logger_setup
from folder_operations import (
    create_directory_if_not_exists,
    copy_subfolders_and_files,
    remove_subfolders_and_files
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
    # Example: python3 main.py src_folder rep_folder 5 events.log
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
