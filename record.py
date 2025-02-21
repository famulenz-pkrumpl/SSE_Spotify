import subprocess

# Absolute path to energibridge executable
energibridge_path = r""
# Absolute path to monitoring service
driver_path = r""

# Service name
service_name = "rapl"
# Absolute path to result directory - path should end with backslash
csv_output_dir_path = r""
timeout_in_seconds = 5


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
    if service_exists(service_name):
        print(f"Service '{service_name}' will be deleted now...")
        run_admin_command(f'sc delete {service_name}')


def setup_service():
    delete_service()

    print(f"Creating Service '{service_name}'...")
    run_admin_command(f'sc create {service_name} type=kernel binPath=\"{driver_path}\"')

    print(f"Starting Service '{service_name}'...")
    run_admin_command(f'sc start {service_name}')


def run_energibridge(output_file_name):
    print("Starting EnergiBridge...")
    result = subprocess.run([energibridge_path, "-o", csv_output_dir_path + output_file_name, "--summary", "timeout", str(timeout_in_seconds)], shell=True)

    if result.returncode == 0:
        print(f"Finished EnergiBridge execution, results are in: '{csv_output_dir_path}'")
    else:
        print("Error executing EnergiBridge")


if __name__ == "__main__":
    setup_service()
    run_energibridge("test1.csv")
    delete_service()
