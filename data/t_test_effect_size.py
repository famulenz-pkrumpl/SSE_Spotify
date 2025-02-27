import pandas as pd
from scipy.stats import ttest_ind
import numpy as np

file_path = "C:/wsl_files/projects/SSE_Spotify/data/no_outliers_results.csv"
df = pd.read_csv(file_path)

web_data = df[df["player"] == "web"]["delta_package_energy_j"]
native_data = df[df["player"] == "native"]["delta_package_energy_j"]

# Perform Welch's t-test
t_stat, p_value = ttest_ind(web_data, native_data, equal_var=False)

mean_web = web_data.mean()
mean_native = native_data.mean()
std_web = web_data.std()
std_native = native_data.std()

mean_diff = mean_native - mean_web

# Percent change (relative to web)
percent_change = (mean_diff / mean_web) * 100

# Cohen’s d
pooled_std = np.sqrt((std_web**2 + std_native**2) / 2)
cohens_d = mean_diff / pooled_std

print(f"Welch’s t-test results:")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print("Result: The difference is statistically significant (reject null hypothesis).")
else:
    print("Result: No significant difference (fail to reject null hypothesis).")

# Effect size results
print("\nEffect Size Analysis:")
print(f"Mean (Web): {mean_web:.4f}")
print(f"Mean (Native): {mean_native:.4f}")
print(f"Mean Difference: {mean_diff:.4f}")
print(f"Percent Change: {percent_change:.2f}%")
print(f"Cohen’s d: {cohens_d:.4f}")

# Cohen's d interpretation
if abs(cohens_d) < 0.2:
    effect_size = "Small"
elif abs(cohens_d) < 0.5:
    effect_size = "Medium"
else:
    effect_size = "Large"

print(f"Effect Size Interpretation: {effect_size} effect")
# Output:
# Welch’s t-test results:
# t-statistic: -9.3391
# p-value: 0.0000
# Result: The difference is statistically significant (reject null hypothesis).
#
# Effect Size Analysis:
# Mean (Web): 625.3481
# Mean (Native): 692.7378
# Mean Difference: 67.3897
# Percent Change: 10.78%
# Cohen’s d: 2.4831
# Effect Size Interpretation: Large effect