import os
import sqlite3
import pandas as pd

cwd = os.getcwd()
csv_dir = os.path.join(cwd, "csv_data")
filenames = os.listdir(csv_dir)
csv_files = [os.path.join(csv_dir, filename) for filename in filenames]

sqlite_db_file = 'stores.db'
conn = sqlite3.connect(sqlite_db_file)

for csv_file, filename in zip(csv_files, filenames):
    table_name = filename.split(".")[0]
    df = pd.read_csv(csv_file)

    # Add a primary key column 'id' if it doesn't exist
    if 'id' not in df.columns:
        df.insert(0, 'id', range(1, len(df) + 1))

    # Save the DataFrame to the SQLite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    print(f"CSV data has been successfully imported into the '{table_name}' table in '{sqlite_db_file}' database.")

conn.commit()
conn.close()
