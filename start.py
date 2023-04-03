import os
import subprocess
import common


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


# Start Process
def start_process_if_not_running(process_name, process_command, pids, env=None):
    if process_name not in pids or not is_process_running(pids[process_name]):
        pids[process_name] = start_process(process_command, env)
    else:
        print(f"{process_name.capitalize()} is already running.")


# Load PIDs from a file or create an empty dictionary
if os.path.exists(common.pid_file):
    with open(common.pid_file, "r") as file:
        pids = {line.split(":")[0]: int(line.split(":")[1]) for line in file.readlines()}
else:
    pids = {}

components = common.config["components"]

for component_name, component_config in components.items():
    folder_pattern = common.get_platform_value(component_config["folder_pattern"])
    binary = common.get_platform_value(component_config["bin"])
    command = common.get_platform_value(component_config["command"])
    env = component_config["env"]

    fq_command = os.path.join(common.install_dir, folder_pattern, binary, command)

    start_process_if_not_running(component_name, fq_command, pids, env)


# Save PIDs to a file for future reference
with open(common.pid_file, "w") as file:
    for key, value in pids.items():
        file.write(f"{key}:{value}\n")

print("Camunda components started successfully.")

