import os
import zipfile
import tarfile
import requests
import platform
import stat
import glob
import common


# Function to download a file from a URL
def download_file(url, file_name):
    target_path = os.path.join(file_name)

    if os.path.exists(target_path):
        print(f"{file_name} already downloaded.")
        return target_path

    print(f"Downloading {file_name}...")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(target_path, 'wb') as target_file:
        for chunk in response.iter_content(chunk_size=8192):
            target_file.write(chunk)

    print(f"{file_name} downloaded.")
    return target_path


# Function to extract a ZIP or TAR.GZ file
def extract_file(filename, extract_directory):
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filename, 'r') as archive:
            archive_files = archive.namelist()
    elif filename.endswith(".tar.gz"):
        with tarfile.open(filename, 'r:gz') as archive:
            archive_files = archive.getnames()

    # Find the common root folder
    extracted_folder = os.path.commonpath(archive_files)
    extracted_path = os.path.join(extract_directory, extracted_folder)

    if not os.path.exists(extracted_path):
        if filename.endswith(".zip"):
            with zipfile.ZipFile(filename, 'r') as archive:
                archive.extractall(path=extract_directory)
        elif filename.endswith(".tar.gz"):
            with tarfile.open(filename, 'r:gz') as archive:
                archive.extractall(path=extract_directory)
        print(f"{filename} extracted to {extract_directory}.")
    else:
        print(f"{extracted_folder} already exists in {extract_directory}. Skipping extraction.")


def set_executable_bit(directory_pattern):
    directories = glob.glob(directory_pattern)
    if not directories:
        print(f"No directories found for pattern: {directory_pattern}")
        return

    if platform.system() in ["Linux", "Darwin"]:
        for directory in directories:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.chmod(file_path, os.stat(file_path).st_mode | stat.S_IEXEC)
                    print(f"Set executable bit for {file_path}")
    else:
        print("Skipping setting executable bit, as the platform is not Linux or macOS.")


def delete_archive_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"{file} deleted.")
        else:
            print(f"{file} does not exist.")


def install(url, local_file, executable_bit_directory, extracted_folder_pattern):
    extracted_folders = glob.glob(extracted_folder_pattern)

    if not extracted_folders:
        download_file(url, local_file)
        extract_file(local_file, common.temp_dir)
        set_executable_bit(executable_bit_directory)
        delete_archive_files(local_file)
    else:
        print(f"The archive from {url} was already installed.")

if not os.path.exists(common.temp_dir):
    os.makedirs(common.temp_dir)

components = common.config["components"]

# Install Camunda components
for component_name, component_config in components.items():

    url = common.get_platform_value(component_config["url"])
    file = os.path.basename(url)
    folder_pattern = common.get_platform_value(component_config["folder_pattern"])
    binary = common.get_platform_value(component_config["bin"])
    command = common.get_platform_value(component_config["command"])

    fq_folder_pattern = os.path.join(common.temp_dir, folder_pattern)
    fq_binary = os.path.join(fq_folder_pattern, binary)
    fq_file = os.path.join(common.temp_dir, os.path.basename(url))

    install(url, fq_file, fq_binary, fq_folder_pattern)


print("Camunda components installed successfully.")
