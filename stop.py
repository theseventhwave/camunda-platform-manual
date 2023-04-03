import os
import common


# Function to stop a process by PID
def stop_process(pid):
    try:
        os.kill(pid, 15)  # Send SIGTERM (15) to gracefully terminate the process
        print(f"Stopped process with PID: {pid}")
    except OSError as e:
        print(f"Could not stop process with PID {pid}. Error: {e}")


# Load PIDs from the file
if os.path.exists(common.pid_file):
    with open(common.pid_file, "r") as file:
        pids = [int(line.split(":")[1]) for line in file.readlines()]

    # Stop processes
    for pid in pids:
        stop_process(pid)

    # Remove pids.txt file
    os.remove(common.pid_file)
else:
    print("No pids.txt file found.")
