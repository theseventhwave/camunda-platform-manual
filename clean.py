import os
import shutil
import common

if os.path.exists(common.install_dir):
    shutil.rmtree(common.install_dir)
    print(f"The '{common.install_dir}' directory has been deleted.")
else:
    print(f"The '{common.install_dir}' directory does not exist.")
