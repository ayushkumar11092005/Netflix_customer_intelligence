import pandas as pd
import os

# 1. Load the master dataset from the cleaned_data folder
cleaned_dir = 'cleaned_data'
master_path = os.path.join(cleaned_dir, 'master_netflix_dataset.csv')

try:
    print("Loading master dataset...")
    df = pd.read_csv(master_path)
    
    print("\n--- DATASET INFO ---")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    
    print("\n--- COLUMN NAMES ---")
    print(list(df.columns))
    
    print("\n--- MISSING VALUES SUMMARY ---")
    missing_data = df.isnull().sum()
    print(missing_data[missing_data > 0])
    
    # Example Insights (Checking Churn Distribution if column exists)
    if 'churn' in df.columns:
        print("\n--- CHURN DISTRIBUTION ---")
        print(df['churn'].value_counts(normalize=True) * 100)
        
    print("\nEDA script executed successfully!")

except Exception as e:
    print(f"An error occurred during EDA: {e}")