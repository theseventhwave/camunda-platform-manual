import os
import zipfile
import tarfile
import requests
import platform
import stat
import glob
import json


def get_platform_value(value, current_platform, current_arch):
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        platform_value = value.get(current_platform)

        if platform_value is None:
            raise ValueError(f"Unsupported platform: {current_platform}")

        if isinstance(platform_value, str):
            return platform_value
        elif isinstance(platform_value, dict):
            if current_arch is None:
                return platform_value  # Return the entire dict if no architecture is provided
            arch_value = platform_value.get(current_arch)

            if arch_value is None:
                raise ValueError(f"Unsupported architecture: {current_arch}")

            return arch_value
        else:
            raise ValueError("Invalid value configuration.")
    else:
        raise ValueError("Invalid value type.")


def recursive_substitute(data, config):
    if isinstance(data, str):
        return data.format(**config)
    elif isinstance(data, list):
        return [recursive_substitute(item, config) for item in data]
    elif isinstance(data, dict):
        return {key: recursive_substitute(value, config) for key, value in data.items()}
    else:
        return data


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)

    return recursive_substitute(config, config)