import os
import shutil
import platform

current_platform = platform.system()

if current_platform not in ["Windows", "Linux", "Darwin"]:
    raise ValueError(f"Unsupported platform: {current_platform}")

temp_dir = "temp"

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
    print(f"The '{temp_dir}' directory has been deleted.")
else:
    print(f"The '{temp_dir}' directory does not exist.")
