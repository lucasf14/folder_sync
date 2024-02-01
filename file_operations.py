import os
import logging
import shutil


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
    elif source_mod_time != replica_mod_time:
        # Update the replica file if the source file was changed
        shutil.copy2(source_file, replica_file)
        logging.info(f"File updated: {source_file} -> {replica_file}")


def remove_files(
    replica_file: str,
    source_file: str
) -> None:
    # Remove files in replica folder that don't exist in source folder
    if not os.path.exists(source_file):
        os.remove(replica_file)
        logging.info(f"File removed: {replica_file}")
