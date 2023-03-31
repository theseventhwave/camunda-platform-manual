import os
import zipfile
import tarfile
import requests
import platform
import stat
import glob


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
        extract_file(local_file, temp_dir)
        set_executable_bit(executable_bit_directory)
        delete_archive_files(local_file)
    else:
        print(f"The archive from {url} was already installed.")


current_platform = platform.system()
current_arch = platform.machine()

if current_platform not in ["Windows", "Linux", "Darwin"]:
    raise ValueError(f"Unsupported platform: {current_platform}")

# Get platform specific URLs
elasticsearch_url = get_elasticsearch_url(current_platform, current_arch)
zeebe_url = "https://github.com/camunda/camunda-platform/releases/download/8.1.9/camunda-zeebe-8.1.9.zip"
operate_url = "https://github.com/camunda/camunda-platform/releases/download/8.1.9/camunda-operate-8.1.9.zip"
tasklist_url = "https://github.com/camunda/camunda-platform/releases/download/8.1.9/camunda-tasklist-8.1.9.zip"

# Get local file names
temp_dir = "temp"
elasticsearch_file = os.path.join(temp_dir, os.path.basename(elasticsearch_url))
zeebe_file = os.path.join(temp_dir, os.path.basename(zeebe_url))
operate_file = os.path.join(temp_dir, os.path.basename(operate_url))
tasklist_file = os.path.join(temp_dir, os.path.basename(tasklist_url))

# Get extracted folder patterns
elasticsearch_folder_pattern = os.path.join(temp_dir, "elasticsearch-*")
zeebe_folder_pattern = os.path.join(temp_dir, "camunda-zeebe-*")
operate_folder_pattern = os.path.join(temp_dir, "camunda-operate-*")
tasklist_folder_pattern = os.path.join(temp_dir, "camunda-tasklist-*")

# Get bin directories
elasticsearch_bin = os.path.join(elasticsearch_folder_pattern, "bin")
zeebe_bin = os.path.join(zeebe_folder_pattern, "bin")
operate_bin = os.path.join(operate_folder_pattern, "bin")
tasklist_bin = os.path.join(tasklist_folder_pattern, "bin")

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Install Camunda components
install(elasticsearch_url, elasticsearch_file, elasticsearch_bin, elasticsearch_folder_pattern)
install(zeebe_url, zeebe_file, zeebe_bin, zeebe_folder_pattern)
install(operate_url, operate_file, operate_bin, operate_folder_pattern)
install(tasklist_url, tasklist_file, tasklist_bin, tasklist_folder_pattern)


print("Camunda components installed successfully.")
