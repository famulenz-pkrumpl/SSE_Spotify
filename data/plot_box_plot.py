import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the parsed results
df = pd.read_csv("data/parsed_results.csv")

# Convert experiment number to string (useful for categorical plotting)
df["experiment_number"] = df["experiment_number"].astype(str)

# Create the plot
plt.figure(figsize=(10, 6))
sns.violinplot(x="player", y="delta_package_energy_j", data=df, inner=None, alpha=0.6)
sns.boxplot(x="player", y="delta_package_energy_j", data=df, width=0.2, showfliers=False)

# Improve labels
plt.xlabel("Player")
plt.ylabel("Energy Used (Joules)")
plt.title("Energy Consumption per Player (Violin + Box Plot)")

# Show the plot
plt.show()