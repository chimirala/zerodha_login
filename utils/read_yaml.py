import yaml
import os
import pathlib


def gen_json(file_path, file_name):
    with open(os.path.join(file_path, file_name)) as f:
        my_dict = yaml.safe_load(f)
    return my_dict


