import os
import subprocess
import platform


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

# Environment variables for Zeebe
zeebe_env = {
    "ZEEBE_BROKER_EXPORTERS_ELASTICSEARCH_CLASSNAME": "io.camunda.zeebe.exporter.ElasticsearchExporter",
    "ZEEBE_BROKER_EXPORTERS_ELASTICSEARCH_ARGS_URL": "http://localhost:9200",
    "ZEEBE_BROKER_EXPORTERS_ELASTICSEARCH_ARGS_BULK_SIZE": "1",
    "ZEEBE_BROKER_DATA_DISKUSAGECOMMANDWATERMARK": "0.998",
    "ZEEBE_BROKER_DATA_DISKUSAGEREPLICATIONWATERMARK": "0.999",
    "JAVA_TOOL_OPTIONS": "-Xms512m -Xmx512m"
}

# Environment variables for Operate
operate_env = {
    "CAMUNDA_OPERATE_ZEEBE_GATEWAYADDRESS": "localhost:26500",
    "CAMUNDA_OPERATE_ELASTICSEARCH_URL": "http://localhost:9200",
    "CAMUNDA_OPERATE_ZEEBEELASTICSEARCH_URL": "http://localhost:9200",
    "SERVER_PORT": "8081"
}

# Environment variables for Tasklist
tasklist_env = {
    "CAMUNDA_TASKLIST_ZEEBE_GATEWAYADDRESS": "localhost:26500",
    "CAMUNDA_TASKLIST_ELASTICSEARCH_URL": "http://localhost:9200",
    "CAMUNDA_TASKLIST_ZEEBEELASTICSEARCH_URL": "http://localhost:9200",
    "SERVER_PORT": "8082"
}

# Environment variables for Elasticsearch
elasticsearch_env = {
    "bootstrap.memory_lock": "true",
    "discovery.type": "single-node",
    "xpack.security.enabled": "false",
    "cluster.routing.allocation.disk.threshold_enabled": "false",
    "ES_JAVA_OPTS": "-Xms512m -Xmx512m"
}

# Start processes with environment variables

if current_platform == "Windows":
    elasticsearch_command = "temp\\elasticsearch-*\\bin\\elasticsearch.bat"
    zeebe_command = "temp\\camunda-zeebe-*\\bin\\broker.bat"
    operate_command = "temp\\camunda-operate-*\\bin\\operate.bat"
    tasklist_command = "temp\\camunda-tasklist-*\\bin\\tasklist.bat"
elif current_platform in ["Linux", "Darwin"]:
    elasticsearch_command = "temp/elasticsearch-*/bin/elasticsearch"
    zeebe_command = "temp/camunda-zeebe-*/bin/broker"
    operate_command = "temp/camunda-operate-*/bin/operate"
    tasklist_command = "temp/camunda-tasklist-*/bin/tasklist"
else:
    raise ValueError("Unsupported platform: {}".format(current_platform))


# Save PIDs to a file for future reference
with open(pid_file, "w") as file:
    for key, value in pids.items():
        file.write(f"{key}:{value}\n")

print("Camunda components started successfully.")

