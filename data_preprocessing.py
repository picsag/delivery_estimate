import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import math

# Read the CSV file
df = pd.read_csv('./data/data.csv')

# Convert 'added' column to datetime format
df['added'] = pd.to_datetime(df['added'])

# Create an intermediary dataframe for sorting
df_sorted = df.sort_values('added')

# Group the sorted data by account_cluster_id
grouped = df_sorted.groupby('account_cluster_id')


# Function to fill missing values using last 7 days' orders for the same city
def fill_missing_values(row):
    cluster_id = row['account_cluster_id']
    order_date = row['added']
    mask = (df_sorted['added'] >= order_date - timedelta(days=6)) & \
           (df_sorted['added'] <= order_date)

    avg_estimated_preptime = math.ceil(df_sorted.loc[mask & (df_sorted['account_cluster_id'] == cluster_id), 'estimated_preptime'].mean())
    avg_actual_preptime = math.ceil(df_sorted.loc[mask & (df_sorted['account_cluster_id'] == cluster_id), 'actual_preptime'].mean())

    if pd.isnull(row['xhist_avg_estimated_preptime']):
        if not pd.isnull(avg_estimated_preptime):
            row['xhist_avg_estimated_preptime'] = avg_estimated_preptime
        else:
            row['xhist_avg_estimated_preptime'] = math.ceil(row['estimated_preptime'])

    if pd.isnull(row['xhist_avg_actual_preptime']):
        if not pd.isnull(avg_actual_preptime):
            row['xhist_avg_actual_preptime'] = avg_actual_preptime
        else:
            row['xhist_avg_actual_preptime'] = math.ceil(row['actual_preptime'])

    return row


# Create a new column to store the original index
df_sorted['original_index'] = df_sorted.index

# Create a new empty dataframe to store the filled values with the correct order
df_filled = pd.DataFrame(columns=df_sorted.columns)

# Apply the fill_missing_values function to each row with a progress bar
progress_bar = tqdm(total=len(df_sorted), desc='Filling missing values')

for index, row in df_sorted.iterrows():
    filled_row = fill_missing_values(row)
    df_filled = pd.concat([df_filled, filled_row.to_frame().transpose()], ignore_index=True)
    progress_bar.update()

progress_bar.close()

# Sort the filled dataframe back to the original order using the original index
df_filled = df_filled.sort_values('original_index')

# Remove the 'original_index' column from the final DataFrame
df_filled.drop('original_index', axis=1, inplace=True)

# Save the filled dataframe to a new CSV file
df_filled.to_csv('./data/data_preprocessed.csv', index=False)
