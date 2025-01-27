import os
from box.exceptions import BoxValueError # type: ignore
import sys
import yaml # type: ignore
from src.ElectricityBill import logging
from src.ElectricityBill.exception import FileOperationError
import json
import joblib # type: ignore
import numpy as np # type: ignore
from ensure import ensure_annotations # type: ignore
from box import ConfigBox # type: ignore
from pathlib import Path
from typing import Any


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            print(content)
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"created directory at: {path}")

# Joblib
def save_object(file_path, obj):
    
    # Get the directory path of the file 
    dir_path = os.path.dirname(file_path)
    # if the directory path does not exist, create it 
    os.makedirs(dir_path, exist_ok = True)

    # save the object in the file 
    with open(file_path, 'wb') as file_obj:
        joblib.dump(obj, file_obj)


def load_object(file_path):

    with open(file_path, 'rb') as file_obj:
        return joblib.load(file_obj)
    
# JSON
@ensure_annotations
def save_json(path: Path, data: dict):

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:

    with open(path) as f:
        content = json.load(f)

    logging.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):

    joblib.dump(value=data, filename=path)
    logging.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:

    data = joblib.load(path)
    logging.info(f"binary file loaded from: {path}")
    return data


# File size
@ensure_annotations
def get_size(path: Path) -> str:

    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"