import os
import subprocess


# Function to start a process and return its PID
def start_process(command):
    process = subprocess.Popen(command, shell=True)
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


# Load PIDs from a file or create an empty dictionary
pid_file = "pids.txt"
if os.path.exists(pid_file):
    with open(pid_file, "r") as file:
        pids = {line.split(":")[0]: int(line.split(":")[1]) for line in file.readlines()}
else:
    pids = {}


# Start Elasticsearch
def start_process_if_not_running(process_name, process_command, pids):
    if process_name not in pids or not is_process_running(pids[process_name]):
        pids[process_name] = start_process(process_command)
    else:
        print(f"{process_name.capitalize()} is already running.")


start_process_if_not_running("elasticsearch", "elasticsearch-*/bin/elasticsearch", pids)
start_process_if_not_running("zeebe", "camunda-zeebe-*/bin/broker", pids)
start_process_if_not_running("operate", "camunda-operate-*/bin/operate", pids)
start_process_if_not_running("tasklist", "camunda-tasklist-*/bin/tasklist", pids)

# Save PIDs to a file for future reference
with open(pid_file, "w") as file:
    for key, value in pids.items():
        file.write(f"{key}:{value}\n")

print("Camunda components started successfully.")
