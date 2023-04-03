import platform
import json


def get_platform_value(value):
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


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


current_platform = platform.system()
current_arch = platform.machine()
config = load_config()

if current_platform not in ["Windows", "Linux", "Darwin"]:
    raise ValueError(f"Unsupported platform: {current_platform}")

temp_dir = config["temp_dir"]
