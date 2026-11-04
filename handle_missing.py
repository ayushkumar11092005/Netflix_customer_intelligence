import pandas as pd
import os

# 1. Load the master dataset from the cleaned_data folder
cleaned_dir = 'cleaned_data'
master_path = os.path.join(cleaned_dir, 'master_netflix_dataset.csv')

df = pd.read_csv(master_path)

print("Missing values before cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# 2. Handle missing values safely
for col in df.columns:
    if df[col].isnull().sum() > 0:
        # Check if the column is numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna('Unknown')

# 3. Save the updated master dataset back
df.to_csv(master_path, index=False)

print("\nAll missing values handled successfully!")
print("Updated Master Dataset Shape:", df.shape)