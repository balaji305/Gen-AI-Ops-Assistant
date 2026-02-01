import pandas as pd
import glob
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

files = glob.glob(os.path.join(DATA_DIR, "../*_2k.log_structured.csv"))

print("🔎 Column Analysis Across Files\n")

for file in files:
    df = pd.read_csv(file, nrows=5)  # read first 5 rows to inspect
    print(f"File: {os.path.basename(file)}")
    print(f"Columns: {list(df.columns)}\n")