# Veeam - Folders Synchronization Test Task

## Overview

This project implements a program that synchronizes two folders: source and replica.
In order to do this, the program should maintain a full, identical copy of the `source folder` in the `replica folder` periodically.


## Used Imports

The project uses the following imports:

- **os:** Used mainly to access file/folder paths, but also to fetch metadata.
- **shutil:** Used to allow file/folder operations, like create, copy and remove.
- **time:** Used to define how often files/folders are synchronized (periodicity).
- **logging:** Used to log information, like the creation, copy and removal of files/folders.
- **argparse:** Used to handle input arguments from the command-line and allow data validation.


## Usage

```bash
python3 main.py <source_folder> <replica_folder> <interval> <log_file>
```


- `source_folder`: Path to the source folder.
- `replica_folder`: Path to the replica folder.
- `interval`: Synchronization interval in seconds.
- `log_file`: Path to the log file.

#### Example
Synchronize folders every 5 seconds:
```bash
python3 main.py source_folder replica_folder 5 event_logger.log
```
