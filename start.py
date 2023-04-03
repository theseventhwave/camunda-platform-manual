import os
import subprocess
import platform
from config import get_platform_value, load_config


# Function to start a process and return its PID
def start_process(command, env=None):
    process = subprocess.Popen(command, shell=True, env=env)
    print(f"Started process with PID: {process.pid}")
    return process.pid


# Function to check if a process is running
def is_process_running(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


current_platform = platform.system()
current_arch = platform.machine()
config = load_config()

if current_platform not in ["Windows", "Linux", "Darwin"]:
    raise ValueError(f"Unsupported platform: {current_platform}")


# Load PIDs from a file or create an empty dictionary
pid_file = "temp/pids.txt"
if os.path.exists(pid_file):
    with open(pid_file, "r") as file:
        pids = {line.split(":")[0]: int(line.split(":")[1]) for line in file.readlines()}
else:
    pids = {}


# Start Process
def start_process_if_not_running(process_name, process_command, pids, env=None):
    if process_name not in pids or not is_process_running(pids[process_name]):
        pids[process_name] = start_process(process_command, env)
    else:
        print(f"{process_name.capitalize()} is already running.")


components = config["components"]

for component_name, component_data in components.items():
    command = get_platform_value(component_data["commands"], current_platform)
    env = component_data["env"]
    start_process_if_not_running(component_name, command, pids, env)


# Save PIDs to a file for future reference
with open(pid_file, "w") as file:
    for key, value in pids.items():
        file.write(f"{key}:{value}\n")

print("Camunda components started successfully.")

