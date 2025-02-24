import os
import csv

def get_delta_package_energy_in_joule(file_path: str) -> float:
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        first_row = next(reader)  # Get the first row
        last_row = None

        for row in reader:
            last_row = row  # Iterate to the last row

    if last_row is None:  # In case there's only one row
        last_row = first_row

    return float(last_row["PACKAGE_ENERGY (J)"]) - float(first_row["PACKAGE_ENERGY (J)"])

folder_path = "data/results_raw"
parsed_results = []

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and "pause" not in filename:  # Skip directories and files containing "pause"
        energy = get_delta_package_energy_in_joule(file_path)
        _, experiment_number, player = filename.replace(".csv", "").split("_")  # Extract metadata
        parsed_results.append([experiment_number, player, energy])

# Write results to a CSV file
output_file = "data/parsed_results.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["experiment_number", "player", "delta_package_energy_j"])  # Write header
    writer.writerows(parsed_results)

print(f"Results saved to {output_file}")
