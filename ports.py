import os
import subprocess
import platform
import common


def get_listening_ports(pid):
    if common.current_platform == "Windows":
        command = f"netstat -ano | findstr /R /C:\" {pid}\""
    elif common.current_platform == "Linux" or common.current_platform == "Darwin":
        command = f"lsof -Pan -p {pid} -iTCP -sTCP:LISTEN"
    else:
        raise NotImplementedError("Unsupported platform")

    output = subprocess.check_output(command, shell=True, text=True)
    ports = set()

    if common.current_platform == "Windows":
        for line in output.splitlines():
            if line.strip():
                ports.add(int(line.split()[-1]))
    else:
        for line in output.splitlines()[1:]:
            if line.strip():
                ports.add(int(line.split()[8].split(":")[-1]))

    return ports


# Load PIDs from the file
if os.path.exists(common.pid_file):
    with open(common.pid_file, "r") as file:
        pids = {line.split(":")[0]: int(line.split(":")[1]) for line in file.readlines()}

    # Get listening ports for each process
    for name, pid in pids.items():
        ports = get_listening_ports(pid)
        if ports:
            print(f"{name.capitalize()} (PID: {pid}) is listening on ports: {', '.join(map(str, ports))}")
        else:
            print(f"No listening ports found for {name.capitalize()} (PID: {pid})")
else:
    print("No pids.txt file found.")
