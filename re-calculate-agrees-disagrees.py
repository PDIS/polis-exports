#!/usr/bin/env python3
# 2023.07.10 by ChatGPT


import pandas as pd
import csv
import os
import sys

# Function to correct the 'agrees' and 'disagrees' fields in the comments.csv file for a specific date
def correct_votes(folder_path):
    # Define the paths to the CSV files
    comments_csv_path = os.path.join(folder_path, 'comments.csv')
    votes_csv_path = os.path.join(folder_path, 'votes.csv')

    # Read the comments.csv file line by line using a CSV reader
    with open(comments_csv_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)
    # Parse the data into a dataframe
    comments_df = pd.DataFrame(data, columns=header)
    comments_df['timestamp'] = pd.to_numeric(comments_df['timestamp'])
    comments_df['comment-id'] = pd.to_numeric(comments_df['comment-id'])
    comments_df['author-id'] = pd.to_numeric(comments_df['author-id'])
    comments_df['agrees'] = pd.to_numeric(comments_df['agrees'])
    comments_df['disagrees'] = pd.to_numeric(comments_df['disagrees'])

    # Load the votes.csv file into a dataframe
    votes_df = pd.read_csv(votes_csv_path)

    # Group by 'comment-id' and 'vote' to get the count of agrees and disagrees for each comment
    votes_count = votes_df.groupby(['comment-id', 'vote']).size().unstack(fill_value=0).reset_index()

    # Rename the columns based on their corresponding vote types
    votes_count.rename(columns={-1: 'disagrees', 1: 'agrees'}, inplace=True)

    # Merge the updated vote counts with the comments dataframe
    comments_df_corrected = pd.merge(comments_df.drop(columns=['agrees', 'disagrees']), votes_count, on='comment-id', how='left')

    # Fill any missing values in 'agrees' and 'disagrees' with 0
    comments_df_corrected[['agrees', 'disagrees']] = comments_df_corrected[['agrees', 'disagrees']].fillna(0)

    # Reorder the columns to put 'agrees' and 'disagrees' before 'moderated'
    columns_order = ['timestamp', 'datetime', 'comment-id', 'author-id', 'agrees', 'disagrees', 'moderated', 'comment-body']
    comments_df_corrected = comments_df_corrected[columns_order]

    # Save the corrected dataframe back to the CSV file, without adding any quotes
    comments_df_corrected.to_csv(comments_csv_path, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

if __name__ == "__main__":
    # Get the date from the command line arguments
    folder_path = sys.argv[1]
    # Call the function to correct the votes
    correct_votes(folder_path)
