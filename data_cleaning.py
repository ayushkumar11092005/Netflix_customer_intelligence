import pandas as pd
import numpy as np
import os

files = [
    'churn_labels.csv',
    'content.csv',
    'customer_feedback (2).csv',
    'payments (2).csv',
    'subscription_plans.csv',
    'subscriptions (1).csv',
    'support_tickets (1).csv',
    'viewing_activity.csv'
]

for file in files:
    file_path = os.path.join('data', file)
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        for col in df.columns:
            # चेक करें कि कॉलम न्यूमेरिकल है या टेक्स्ट
            if pd.api.types.is_numeric_dtype(df[col]):
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val if not pd.isna(median_val) else 0)
            else:
                df[col] = df[col].fillna('Unknown')
                
        df.drop_duplicates(inplace=True)
        
        output_name = file.replace(' (2)', '').replace(' (3)', '').replace(' (1)', '')
        output_path = os.path.join('cleaned_data', f'{output_name.split(".")[0]}_cleaned.csv')
        
        df.to_csv(output_path, index=False)
        print(f"Cleaned and Saved: {output_name}")
    else:
        print(f"File not found: {file}")

print("\nAll remaining files cleaned successfully!")