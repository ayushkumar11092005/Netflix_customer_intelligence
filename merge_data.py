import pandas as pd
import os

# 1. Define the path for the cleaned data directory
cleaned_dir = 'cleaned_data'

try:
    # 2. Load the cleaned CSV files using their exact filenames
    print("Loading cleaned datasets...")
    customers_df = pd.read_csv(os.path.join(cleaned_dir, 'customers_cleaned.csv'))
    subscriptions_df = pd.read_csv(os.path.join(cleaned_dir, 'subscriptions_cleaned.csv'))
    payments_df = pd.read_csv(os.path.join(cleaned_dir, 'payments_cleaned.csv'))
    churn_df = pd.read_csv(os.path.join(cleaned_dir, 'churn_labels_cleaned.csv'))
    viewing_df = pd.read_csv(os.path.join(cleaned_dir, 'viewing_activity_cleaned.csv'))
    
    # 3. Merge datasets step-by-step using 'customer_id'
    print("Merging datasets...")
    master_df = pd.merge(customers_df, subscriptions_df, on='customer_id', how='left')
    master_df = pd.merge(master_df, payments_df, on='customer_id', how='left')
    master_df = pd.merge(master_df, churn_df, on='customer_id', how='left')
    master_df = pd.merge(master_df, viewing_df, on='customer_id', how='left')

    # 4. Save the final master dataset inside the cleaned_data folder
    output_path = os.path.join(cleaned_dir, 'master_netflix_dataset.csv')
    master_df.to_csv(output_path, index=False)

    print("Success! All cleaned files have been merged into 'master_netflix_dataset.csv'.")
    print("Master Dataset Shape (Rows, Columns):", master_df.shape)

except Exception as e:
    print(f"An error occurred during merging: {e}")