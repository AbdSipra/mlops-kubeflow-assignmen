import pandas as pd
import numpy as np

# Boston housing data from the original CMU source
data_url = "http://lib.stat.cmu.edu/datasets/boston"

# Read the raw text data
raw_df = pd.read_csv(data_url, sep=r"\s+", skiprows=22, header=None)

# This reshapes the weird text format into a proper matrix (copying logic from sklearn message)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

# Create a DataFrame; generic feature names are fine for this assignment
num_features = data.shape[1]
feature_names = [f"f{i}" for i in range(num_features)]

df = pd.DataFrame(data, columns=feature_names)
df["TARGET"] = target

# Save to CSV
df.to_csv("data/raw_data.csv", index=False)
print("Saved data/raw_data.csv")
