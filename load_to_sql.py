import pandas as pd
import sqlite3
import os

# 1. Load the cleaned master dataset
master_path = os.path.join('cleaned_data', 'master_netflix_dataset.csv')
print("Loading master dataset...")
df = pd.read_csv(master_path)
print(f"Loaded rows: {df.shape[0]}, columns: {df.shape[1]}")

# 2. Create/Connect to SQLite database
db_name = 'netflix_customer_intelligence.db'
conn = sqlite3.connect(db_name)

# 3. Write data to SQLite table
print("Populating data into SQL database...")
df.to_sql('netflix_data', conn, if_exists='replace', index=False)

# 4. Verify table row count
query = "SELECT COUNT(*) FROM netflix_data;"
count = pd.read_sql(query, conn).iloc[0, 0]
print(f"Success! Total rows in database table 'netflix_data': {count}")

conn.close()