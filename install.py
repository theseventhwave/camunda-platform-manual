import os
import zipfile
import tarfile
import requests
import platform
import stat
import glob
from urllib.parse import urlparse


# Function to download a file from a URL
def download_file(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    target_path = os.path.join("temp", file_name)

    if os.path.exists(target_path):
        print(f"{file_name} already downloaded.")
        return target_path

    print(f"Downloading {file_name}...")

    if not os.path.exists("temp"):
        os.makedirs("temp")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(target_path, 'wb') as target_file:
        for chunk in response.iter_content(chunk_size=8192):
            target_file.write(chunk)

    print(f"{file_name} downloaded.")
    return target_path


# Function to extract a ZIP or TAR.GZ file
def extract_file(filename):
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filename, 'r') as archive:
            archive_files = archive.namelist()
    elif filename.endswith(".tar.gz"):
        with tarfile.open(filename, 'r:gz') as archive:
            archive_files = archive.getnames()

    # Find the common root folder
    extracted_folder = os.path.commonpath(archive_files)

    if not os.path.exists(extracted_folder):
        if filename.endswith(".zip"):
            with zipfile.ZipFile(filename, 'r') as archive:
                archive.extractall()
        elif filename.endswith(".tar.gz"):
            with tarfile.open(filename, 'r:gz') as archive:
                archive.extractall()
        print(f"{filename} extracted.")
    else:
        print(f"{extracted_folder} already exists. Skipping extraction.")


def get_elasticsearch_url(current_platform, current_arch):
    if current_platform == 'Windows':
        return 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.2-windows-x86_64.zip'
    elif current_platform == 'Darwin':
        if current_arch == 'x86_64':
            return 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.2-darwin-x86_64.tar.gz'
        else:
            return 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.2-darwin-aarch64.tar.gz'
    elif current_platform == 'Linux':
        if current_arch == 'x86_64':
            return 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.2-linux-x86_64.tar.gz'
        else:
            return 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.2-linux-aarch64.tar.gz'
    else:
        raise ValueError(f"Unsupported platform: {current_platform}")


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


current_platform = platform.system()
current_arch = platform.machine()

# Get platform specific URLs
elasticsearch_url = get_elasticsearch_url(current_platform, current_arch)
zeebe_url = "https://github.com/camunda/camunda-platform/releases/download/8.1.9/camunda-zeebe-8.1.9.zip"
operate_url = "https://github.com/camunda/camunda-platform/releases/download/8.1.9/camunda-operate-8.1.9.zip"
tasklist_url = "https://github.com/camunda/camunda-platform/releases/download/8.1.9/camunda-tasklist-8.1.9.zip"

# Get local file names
elasticsearch_file = os.path.basename(elasticsearch_url)
zeebe_file = os.path.basename(zeebe_url)
operate_file = os.path.basename(operate_url)
tasklist_file = os.path.basename(tasklist_url)

# Download and extract Camunda components
download_file(elasticsearch_url)
download_file(zeebe_url)
download_file(operate_url)
download_file(tasklist_url)

extract_file(elasticsearch_file)
extract_file(zeebe_file)
extract_file(operate_file)
extract_file(tasklist_file)

set_executable_bit("elasticsearch-*/bin")
set_executable_bit("camunda-zeebe-*/bin")
set_executable_bit("camunda-operate-*/bin")
set_executable_bit("camunda-tasklist-*/bin")

print("Camunda components installed successfully.")
