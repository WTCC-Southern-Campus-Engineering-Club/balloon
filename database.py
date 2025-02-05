from __future__ import annotations

import csv
import logging
import os
import random
import time
import typing

from constants import *

database_logger = logging.getLogger('balloon.database')

class DataPoint:
    def __init__(self, **kwargs: dict[str, typing.Any]) -> None:
        self.data = kwargs
        self.created = time.time()

    @property
    def values(self):
        return list(self.data.keys())

    def __getattr__(self, name) -> typing.Any | None:
        if name in self.data:
            return self.data[name]
        else:
            return None

data = {}
tracked_data_types = []

def ensure_database_exists(filename: str) -> bool:
    """
    Ensure the CSV exists, and if not, create it.
    :param filename: database file name
    :return: whether the file exists AFTER the function execution: i.e. whether it succeeded
    """
    global tracked_data_types, data
    # Logger
    log = database_logger.getChild("ensure_database_exists")

    if not os.path.exists(filename):  # Does the file exist?
        try:

            with open(filename, mode='w', newline='') as file:  # Try to create the file
                writer = csv.writer(file)
                writer.writerow([])  # Blank, dynamically updated header
            log.debug(f"Successfully created database file {filename!r}.")
            return True

        # Failed to create the file
        except PermissionError:
            log.debug(f"Failed to create database file {filename!r}: Permission denied.")
        except OSError as e:
            log.debug(f"Failed to create database file {filename!r}: OS error - {e}")
        return False

    else:  # File is already there :)
        log.debug(f"Failed to create database file {filename!r}: already exists.")
        with open(filename, mode='r', newline='') as file:  # Try to create the file
            reader = csv.DictReader(file)
            tracked_data_types = reader.fieldnames
            if tracked_data_types is None:
                tracked_data_types = []
            data = {}
            other_data = [dict(d) for d in reader]
            for dt in tracked_data_types:
                data[dt] = []
            for line in other_data:
                for key in line:
                    data[key].append(line[key])

        return True



ensure_database_exists(DB_FILENAME)


def save_datapoint(datapoint: DataPoint) -> bool:
    data_types = datapoint.values
    for data_type in data_types:
        if data_type not in tracked_data_types:
            tracked_data_types.append(data_type)

    random.shuffle(tracked_data_types)

    with open(DB_FILENAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        existing_data = [dict(d) for d in reader]

    with open(DB_FILENAME, mode='w', newline='') as file:
        existing_data.append(datapoint.data)
        writer = csv.DictWriter(file, fieldnames=tracked_data_types)
        writer.writeheader()
        writer.writerows(existing_data)
