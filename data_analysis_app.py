"""
Codomax Python Internship - Module 4: Python Data & APIs
Project: Data Analysis & REST API Consumer Application
Features:
  - REST API consumption via HTTP requests (JSON payload parsing)
  - Data cleaning, transformation, and manipulation with Pandas & NumPy
  - Visual plotting using Matplotlib & Seaborn
  - Automated statistical summary report generation
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

API_URL = "https://jsonplaceholder.typicode.com/posts"
PROCESSED_CSV = "cleaned_api_data.csv"
REPORT_FILE = "data_analysis_report.txt"
CHART_FILE = "posts_length_distribution.png"


def fetch_api_data(url: str) -> list:
    """Fetches data from a REST API endpoint and handles HTTP errors."""
    print(f"🌐 Fetching live REST API data from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Successfully retrieved {len(data)} records.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Failed: {e}")
        return []


def process_and_clean_data(raw_data: list) -> pd.DataFrame:
    """Cleans, manipulates, and transforms dataset using Pandas and NumPy."""
    df = pd.DataFrame(raw_data)
    if df.empty:
        return df

    # Feature Engineering
    df['title_length'] = df['title'].apply(lambda x: len(str(x)))
    df['body_word_count'] = df['body'].apply(lambda x: len(str(x).split()))
    
    # NumPy calculations
    df['normalized_score'] = np.round(
        (df['body_word_count'] - np.mean(df['body_word_count'])) / np.std(df['body_word_count']), 2
    )

    # Clean missing/null values if any exist
    df.dropna(subset=['title', 'body'], inplace=True)

    # Export cleaned dataset
    df.to_csv(PROCESSED_CSV, index=False)
    print(f"💾 Cleaned dataset exported to '{PROCESSED_CSV}'.")
    return df


def generate_visualizations(df: pd.DataFrame):
    """Generates visual charts using Seaborn and Matplotlib."""
    if df.empty:
        return

    plt.figure(figsize=(10, 5))
    sns.set_theme(style="whitegrid")

    # Subplot 1: Distribution of Body Word Counts
    plt.subplot(1, 2, 1)
    sns.histplot(df['body_word_count'], kde=True, color="#2563eb", bins=12)
    plt.title("Post Word Count Distribution")
    plt.xlabel("Word Count")
    plt.ylabel("Frequency")

    # Subplot 2: User Activity / Post Counts
    plt.subplot(1, 2, 2)
    user_counts = df['userId'].value_counts().sort_index()
    sns.barplot(x=user_counts.index, y=user_counts.values, palette="Blues_r")
    plt.title("Total Posts per User ID")
    plt.xlabel("User ID")
    plt.ylabel("Post Count")

    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=300)
    plt.close()
    print(f"📊 Visualization chart exported to '{CHART_FILE}'.")


def generate_statistical_report(df: pd.DataFrame):
    """Generates a text report with statistical metrics."""
    if df.empty:
        return

    report = f"""==================================================
CODOMAX PYTHON INTERNSHIP: MODULE 4 ANALYSIS REPORT
==================================================
Total Records Processed: {len(df)}
Total Unique Users: {df['userId'].nunique()}

Statistical Summary (Body Word Count):
- Mean Word Count: {df['body_word_count'].mean():.2f}
- Median Word Count: {df['body_word_count'].median():.2f}
- Standard Deviation: {df['body_word_count'].std():.2f}
- Max Word Count: {df['body_word_count'].max()}
- Min Word Count: {df['body_word_count'].min()}

Statistical Summary (Title Character Length):
- Mean Title Length: {df['title_length'].mean():.2f}
- Max Title Length: {df['title_length'].max()}
- Min Title Length: {df['title_length'].min()}

Report Generated Successfully.
==================================================
"""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"📝 Summary report generated in '{REPORT_FILE}'.\n")
    print(report)


def main():
    raw_data = fetch_api_data(API_URL)
    if raw_data:
        df = process_and_clean_data(raw_data)
        generate_visualizations(df)
        generate_statistical_report(df)


if __name__ == "__main__":
    main()