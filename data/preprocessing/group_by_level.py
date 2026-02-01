import pandas as pd
import glob
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Only the 7 relevant files
files_to_check = [
    "HPC_2k.log_structured.csv",
    "Linux_2k.log_structured.csv",
    "Spark_2k.log_structured.csv",
    "Android_2k.log_structured.csv",
    "Windows_2k.log_structured.csv",
    "HDFS_2k.log_structured.csv",
    "Apache_2k.log_structured.csv"
]

print("🔎 Log Level Counts per File\n")

for file_name in files_to_check:
    path = os.path.join(DATA_DIR, "../"+file_name)
    df = pd.read_csv(path)
    
    # Map column names for level
    if 'Level' in df.columns:
        level_col = 'Level'
    elif 'State' in df.columns:
        level_col = 'State'
    elif 'Flag' in df.columns:
        level_col = 'Flag'
    else:
        print(f"{file_name}: No level column found, skipping")
        continue
    
    counts = df[level_col].value_counts()
    print(f"{file_name}:")
    print(counts, "\n")
