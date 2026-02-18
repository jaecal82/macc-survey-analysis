import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    # 1. Read the CSV, skipping the second header row (row index 1)
    # The prompt implies we need to handle the structure where row 0 is header,
    # row 1 is question text (index 0 in df), row 2 is import id (index 1 in df).
    # We read with header=0 to get column names (Q35_1 etc).
    try:
        df = pd.read_csv("data/survey_data.csv")
    except FileNotFoundError:
        print("Error: data/survey_data.csv not found. Please run src/convert_data.py first.")
        return

    # 2. Select columns Q35_1 through Q35_10
    # We filter for columns starting with Q35_ to be dynamic, or we can list them explicitly.
    # Given the prompt, let's find all available Q35 columns.
    q35_cols = [c for c in df.columns if c.startswith("Q35_")]

    if not q35_cols:
        print("No Q35 columns found.")
        return

    # Extract course names from row index 0 (Question Text)
    # Format: "... - COURSE NAME"
    rename_map = {}
    for col in q35_cols:
        # row index 0 in dataframe corresponds to the second line of the file (Question Text)
        question_text = str(df.iloc[0][col])
        if " - " in question_text:
            course_name = question_text.split(" - ")[-1].strip()
            rename_map[col] = course_name
        else:
            rename_map[col] = col # Fallback

    # Select the columns
    df_subset = df[q35_cols].copy()

    # 3. Rename columns
    df_subset.rename(columns=rename_map, inplace=True)

    # 4. Clean and reshape the data
    # Drop the first two rows:
    # Index 0: Question Text (used for renaming)
    # Index 1: ImportId (metadata)
    df_clean = df_subset.iloc[2:].copy()

    # Convert to numeric, coercing errors to NaN
    # Ranking data should be integers (1-N).
    for col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # 5. Calculate the average rank for each course
    # Lower rank (1) is better.
    average_ranks = df_clean.mean().sort_values(ascending=True)

    # 6. Print the final rank-ordered list to the console
    print("Rank order of MAcc CORE courses (based on student ratings, lower is better):")
    print(average_ranks)

    # 7. Save a bar chart of the average rankings
    plt.figure(figsize=(12, 8)) # Larger figure for readable labels
    # Use a bar chart
    average_ranks.plot(kind='bar', color='skyblue', edgecolor='black')

    plt.title("Average Course Rankings (Lower is Better)")
    plt.ylabel("Average Rank")
    plt.xlabel("Course")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    output_path = "outputs/rank_order.png"
    plt.savefig(output_path)
    print(f"Saved chart to {output_path}")

if __name__ == "__main__":
    main()
