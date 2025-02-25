import pandas as pd
from scipy.stats import zscore, shapiro


def remove_outliers(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # Compute the mean delta_package_energy_j
    df_grouped = df.groupby(["experiment_number", "player"], as_index=False)["delta_package_energy_j"].mean()

    # Compute z-scores for each player type
    df_grouped["z_score"] = df_grouped.groupby("player")["delta_package_energy_j"].transform(lambda x: zscore(x))

    # Filter out outliers (absolute z-score <= 3)
    df_cleaned = df_grouped[abs(df_grouped["z_score"]) <= 3].drop(columns=["z_score"])

    df_cleaned.to_csv(output_csv, index=False)

    # Perform Shapiro-Wilk test for normality
    for player in df_cleaned["player"].unique():
        subset = df_cleaned[df_cleaned["player"] == player]["delta_package_energy_j"]
        stat, p = shapiro(subset)
        print(f"Shapiro-Wilk test for {player}: W={stat:.4f}, p-value={p:.4f}")


# Example usage
input_file = "C:/wsl_files/projects/SSE_Spotify/data/parsed_results.csv"
output_file = "C:/wsl_files/projects/SSE_Spotify/data/no_outliers_results.csv"
# Run twice to ensure data is normal
remove_outliers(input_file, output_file)
remove_outliers(output_file, output_file)
# Output:
# First run:
# Shapiro-Wilk test for web: W=0.8517, p-value=0.0008
# Shapiro-Wilk test for native: W=0.9882, p-value=0.9809
# Second run:
# Shapiro-Wilk test for web: W=0.9573, p-value=0.3002
# Shapiro-Wilk test for native: W=0.9882, p-value=0.9809

