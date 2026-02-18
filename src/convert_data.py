import pandas as pd
import os

# Define file paths
input_file = "Grad Program Exit Survey Data 2024 (1).xlsx"
output_file = "data/survey_data.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Read the Excel file
# We read with header=0 to get the first row as headers, matching typical pandas behavior
# This preserves the structure: Row 0 -> Header, Row 1 -> Data Index 0 (Question Text), etc.
df = pd.read_excel(input_file)

# Save as CSV
df.to_csv(output_file, index=False)

print(f"Successfully converted {input_file} to {output_file}")
