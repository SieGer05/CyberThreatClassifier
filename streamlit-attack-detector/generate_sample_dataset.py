import os
import pandas as pd
import random

folder_path = 'dataset'

file_names = [f for f in os.listdir(folder_path) if f.endswith('.csv') and os.path.isfile(os.path.join(folder_path, f))]
print("Files found:", file_names)

dataframes = []
for file in file_names:
   file_path = os.path.join(folder_path, file)
   df = pd.read_csv(file_path, low_memory=False)
   
   if 'Label' in df.columns:
      df = df.drop(columns=['Label'])

   dataframes.append(df)

full_data = pd.concat(dataframes, ignore_index=True)

sample_data = full_data.sample(n=100, random_state=42)

sample_data.to_csv("sample.csv", index=False)
print("====== sample.csv generated with 100 random rows ======")