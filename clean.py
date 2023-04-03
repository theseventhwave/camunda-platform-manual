import os
import shutil
import common

if os.path.exists(common.temp_dir):
    shutil.rmtree(common.temp_dir)
    print(f"The '{common.temp_dir}' directory has been deleted.")
else:
    print(f"The '{common.temp_dir}' directory does not exist.")
