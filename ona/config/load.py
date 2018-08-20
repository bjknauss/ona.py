from os import path
import yaml


def get_config_dir():
    '''Get path to directory containing config YAML files.'''
    current_directory = path.dirname(__file__)
    return path.join(current_directory, '../../config')


def load_config(filename: str) -> dict:
    '''Load config file from the config folder'''
    config_dir = get_config_dir()
    fullpath = path.join(config_dir, filename)
    with open(fullpath, 'r') as yml_file:
        return yaml.load(yml_file)
