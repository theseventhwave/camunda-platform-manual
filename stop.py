import os
import platform


# Function to stop a process by PID
def stop_process(pid):
    try:
        os.kill(pid, 15)  # Send SIGTERM (15) to gracefully terminate the process
        print(f"Stopped process with PID: {pid}")
    except OSError as e:
        print(f"Could not stop process with PID {pid}. Error: {e}")


current_platform = platform.system()

if current_platform not in ["Windows", "Linux", "Darwin"]:
    raise ValueError(f"Unsupported platform: {current_platform}")

# Load PIDs from the file
pid_file = "temp/pids.txt"
if os.path.exists(pid_file):
    with open(pid_file, "r") as file:
        pids = [int(line.split(":")[1]) for line in file.readlines()]

    # Stop processes
    for pid in pids:
        stop_process(pid)

    # Remove pids.txt file
    os.remove(pid_file)
else:
    print("No pids.txt file found.")
