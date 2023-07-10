#!/usr/bin/env python3
# 2023.07.10 by ChatGPT

import pandas as pd
import re
import os
import argparse
from pathlib import Path

def clean_comments_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    cleaned_content = re.sub(r'\n"', '"', content)
    with open(file_path, "w") as file:
        file.write(cleaned_content)
    df = pd.read_csv(file_path)
    return df

def process_files(directory_path):
    comments_file_path = os.path.join(directory_path, 'comments.csv')
    votes_file_path = os.path.join(directory_path, 'votes.csv')

    # Clean and load comments.csv
    df_comments = clean_comments_file(comments_file_path)
    
    # Load votes.csv
    df_votes = pd.read_csv(votes_file_path)
    
    # Sort both DataFrames by 'timestamp'
    df_comments_sorted = df_comments.sort_values(by='timestamp')
    df_votes_sorted = df_votes.sort_values(by='timestamp')
    
    # Filter out rows where 'moderated' is -1 in comments.csv
    df_comments_filtered = df_comments_sorted[df_comments_sorted['moderated'] != -1]
    
    # Remove rows in votes.csv where 'comment-id' is not in the filtered comments.csv
    df_votes_filtered = df_votes_sorted[df_votes_sorted['comment-id'].isin(df_comments_filtered['comment-id'])]
    
    # Overwrite the original files with the filtered DataFrames
    df_comments_filtered.to_csv(comments_file_path, index=False)
    df_votes_filtered.to_csv(votes_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process comments.csv and votes.csv in the given directory.')
    parser.add_argument('dir_path', help='The directory containing comments.csv and votes.csv')
    args = parser.parse_args()
    
    process_files(args.dir_path)
