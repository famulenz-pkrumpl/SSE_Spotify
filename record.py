import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

ENERGIBRIDGE_PATH = os.getenv("ENERGIBRIDGE_PATH")
DRIVER_PATH = os.getenv("DRIVER_PATH")
SERVICE_NAME = os.getenv("SERVICE_NAME")
CSV_OUTPUT_DIR_PATH = os.getenv("CSV_OUTPUT_DIR_PATH")


def run_admin_command(command):
    full_command = f'powershell -Command "Start-Process cmd -ArgumentList \'/c {command}\' -Verb RunAs"'
    subprocess.run(full_command, shell=True)


def service_exists(service):
    try:
        result = subprocess.run(f'sc query {service}', shell=True, capture_output=True, text=True)
        # FAILED 1060 = Service not Found
        return "FAILED 1060" not in result.stdout
    except Exception as e:
        print(f"Error: {e}")
        return False


def delete_service():
    if service_exists(SERVICE_NAME):
        print(f"Service '{SERVICE_NAME}' will be deleted now...")
        run_admin_command(f'sc delete {SERVICE_NAME}')


def setup_service():
    delete_service()

    print(f"Creating Service '{SERVICE_NAME}'...")
    run_admin_command(f'sc create {SERVICE_NAME} type=kernel binPath=\"{DRIVER_PATH}\"')

    print(f"Starting Service '{SERVICE_NAME}'...")
    run_admin_command(f'sc start {SERVICE_NAME}')


def run_energibridge(output_file_name, timeout_in_seconds):
    print("Starting EnergiBridge...")
    result = subprocess.Popen([ENERGIBRIDGE_PATH, "-o", CSV_OUTPUT_DIR_PATH + output_file_name, "--summary", "timeout", str(timeout_in_seconds)], shell=True)

    if result.returncode == 0:
        print(f"Finished EnergiBridge execution, results are in: '{CSV_OUTPUT_DIR_PATH}'")
    else:
        print("Error executing EnergiBridge")

    return result


if __name__ == "__main__":
    setup_service()
    run_energibridge("test1.csv", 5)
    delete_service()
