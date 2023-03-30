import os
import re
import shutil

# Define regular expressions to match the directory names
elasticsearch_regex = re.compile(r"^elasticsearch-\d+\.\d+\.\d+$")
zeebe_regex = re.compile(r"^camunda-zeebe-\d+\.\d+\.\d+$")
operate_regex = re.compile(r"^camunda-operate-\d+\.\d+\.\d+$")
tasklist_regex = re.compile(r"^camunda-tasklist-\d+\.\d+\.\d+$")

# Define a dictionary of regular expressions and corresponding names
dirs_to_delete = {
    elasticsearch_regex: "elasticsearch",
    zeebe_regex: "zeebe",
    operate_regex: "operate",
    tasklist_regex: "tasklist"
}

# Iterate over the directories and delete the matching ones
for dirpath, dirnames, filenames in os.walk("."):
    for regex, name in dirs_to_delete.items():
        if regex.match(os.path.basename(dirpath)):
            shutil.rmtree(dirpath)
            print(f"{name} directory deleted.")