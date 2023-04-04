# Camunda Platform 8 Local Runner

This project allows you to run key components of the Camunda Platform 8 engine on your local machine without needing Docker. This is especially useful for organizations that do not allow hypervisors to be run within their organizational boundaries for security reasons.

## Dependencies

To use this project, you will need the following dependencies installed on your machine:

- Python 3.6 or later
- Java 11 or later (JVM)

## Components

The components included in this project are:

- Elasticsearch
- Zeebe
- Operate
- Tasklist

## Setup and Usage

1. Clone the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run `install.py` to download and install the Camunda components:

    ```bash
    python install.py
    ```

4. Start the Camunda components by running `start.py`:

    ```bash
    python start.py
    ```

5. To check the ports on which the components are running, run `ports.py`:

    ```bash
    python ports.py
    ```

6. When you are done, stop the Camunda components by running `stop.py`:

    ```bash
    python stop.py
    ```

7. If you want to clean up the installed components and remove their directories, run `clean.py`:

    ```bash
    python clean.py
    ```

## Troubleshooting

If you encounter any issues while running the Camunda Local Runner, try the following steps to resolve them:

1. **Check if all components were downloaded and installed correctly**: Ensure that the `install.py` script completed without any errors. If there were issues during the installation, try running the script again.

2. **Check if the processes are running**: If some components are not starting or functioning as expected, check if their processes are running using the `ports.py` script. This will show you the listening ports for each component. If a component is not running, try starting it again using the `start.py` script.

3. **Check logs for errors**: Each component generates logs in its respective folder within the installation directory. Check the logs for any error messages or exceptions that could help you identify the cause of the problem.

4. **Ensure Java is installed and properly configured**: Make sure that you have the required version of Java (Java 11 or later) installed on your system and that the `JAVA_HOME` environment variable is correctly set.

5. **Check for port conflicts**: If you see errors related to ports being already in use, it's possible that other applications or services on your machine are using the same ports as the Camunda components. You can either stop the conflicting applications or services, or update the configuration files for the Camunda components to use different ports.

6. **Restart the components**: If all else fails, you can try stopping the components using the `stop.py` script and then starting them again using the `start.py` script.

If you are still experiencing issues, you can create an issue in the project repository, providing details about the problem and any error messages or logs that could help diagnose the issue.
