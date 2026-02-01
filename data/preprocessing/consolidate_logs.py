import pandas as pd
import glob
import os
import random

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(DATA_DIR, "../consolidated_logs.csv")
SAMPLE_FILE = os.path.join(DATA_DIR, "../logs_sample_20.csv")

# 7 relevant files
files_to_process = [
    "HPC_2k.log_structured.csv",
    "Linux_2k.log_structured.csv",
    "Spark_2k.log_structured.csv",
    "Android_2k.log_structured.csv",
    "Windows_2k.log_structured.csv",
    "HDFS_2k.log_structured.csv",
    "Apache_2k.log_structured.csv"
]

# Severity mapping per original level
LEVEL_MAPPING = {
    # INFO group
    'INFO': 'INFO', 'Info': 'INFO', 'I': 'INFO', 'notice': 'INFO',
    'temperature': 'INFO', 'status': 'INFO', 'start': 'INFO', 'success': 'INFO', 'new': 'INFO',
    # WARN group
    'WARN': 'WARN', 'W': 'WARN', 'fdmn.full': 'WARN', 'temphigh': 'WARN', 'net.niff.up': 'WARN', 'net.niff.down': 'WARN',
    # ERROR group
    'ERROR': 'ERROR', 'E': 'ERROR', 'error': 'ERROR', 'abort': 'ERROR', 'bcast-error': 'ERROR', 'fdmn.panic': 'ERROR'
}

def map_level(level):
    return LEVEL_MAPPING.get(str(level).strip(), 'INFO')  # default INFO if unknown

def add_synthetic_severity(df, level_col='level', fraction=0.05):
    """Upgrade some INFO logs to WARN/ERROR for KG prototype."""
    info_indices = df[df[level_col] == 'INFO'].index.tolist()
    sample_count = max(1, int(len(info_indices) * fraction))
    sampled_indices = random.sample(info_indices, sample_count)
    for i in sampled_indices:
        df.at[i, level_col] = random.choice(['WARN', 'ERROR'])
    return df

all_logs = []

for file_name in files_to_process:
    path = os.path.join(DATA_DIR, "../"+file_name)
    df = pd.read_csv(path)
    category = file_name.split('_')[0]  # e.g., 'HPC', 'Linux', 'Apache'
    
    # Determine level column
    if 'Level' in df.columns:
        level_col = 'Level'
    elif 'State' in df.columns:
        level_col = 'State'
    elif 'Flag' in df.columns:
        level_col = 'Flag'
    else:
        level_col = None
    
    # Standardize timestamp
    if 'Time' in df.columns and 'Date' in df.columns:
        df['timestamp'] = df['Date'].astype(str) + " " + df['Time'].astype(str)
    elif 'Time' in df.columns:
        df['timestamp'] = df['Time']
    else:
        df['timestamp'] = pd.NaT  # optional
    
    # Service
    if 'Component' in df.columns:
        df['service'] = df['Component']
    else:
        df['service'] = category
    
    # Level mapping
    if level_col:
        df['level'] = df[level_col].map(map_level)
    else:
        df['level'] = 'INFO'  # default
    
    # Message
    if 'Content' in df.columns:
        df['message'] = df['Content']
    elif 'EventTemplate' in df.columns:
        df['message'] = df['EventTemplate']
    else:
        df['message'] = ''
    
    # Incident ID
    if 'EventId' in df.columns:
        df['incident_id'] = df['EventId']
    else:
        df['incident_id'] = [f"{category}-{i+1}" for i in range(len(df))]
    
    # Category
    df['category'] = category
    
    # Synthetic variation if all INFO
    if df['level'].nunique() == 1 and df['level'].iloc[0] == 'INFO':
        df = add_synthetic_severity(df, level_col='level', fraction=0.05)
    
    # Keep only required columns
    df = df[['timestamp', 'service', 'level', 'message', 'incident_id', 'category']]
    all_logs.append(df)

# Concatenate all logs
consolidated_df = pd.concat(all_logs, ignore_index=True)

# Save full dataset
consolidated_df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Consolidated logs saved to {OUTPUT_FILE}")

# Save sample 20 logs for KG prototype
sample_df = consolidated_df.sample(n=20, random_state=42)
sample_df.to_csv(SAMPLE_FILE, index=False)
print(f"✅ Sample 20 logs saved to {SAMPLE_FILE}")