import pandas as pd
from datetime import datetime, timedelta
import math
import unittest


# Define a test case class
class TestPrepTimes(unittest.TestCase):

    def setUp(self):
        # Read the filled CSV file
        self.df_filled = pd.read_csv('./data/data_preprocessed.csv')

        # Convert 'added' column to datetime format
        self.df_filled['added'] = pd.to_datetime(self.df_filled['added'])

        # Group the data by account_cluster_id
        self.grouped = self.df_filled.groupby('account_cluster_id')

    def test_avg_preptime(self):
        # Iterate over each row in the dataframe
        for _, row in self.df_filled.iterrows():
            print(row)
            cluster_id = row['account_cluster_id']
            order_date = row['added']

            # Calculate the date range for the last 7 days
            date_range = pd.date_range(end=order_date, periods=8, freq='D')

            # Filter the grouped dataframe for the same cluster and within the date range
            mask = (self.grouped.get_group(cluster_id)['added'] >= order_date - timedelta(days=6)) & \
                   (self.grouped.get_group(cluster_id)['added'] <= order_date)

            # Calculate the average estimated preptime and actual preptime
            avg_estimated_preptime = math.ceil(self.grouped.get_group(cluster_id).loc[mask, 'estimated_preptime'].mean())
            avg_actual_preptime = math.ceil(self.grouped.get_group(cluster_id).loc[mask, 'actual_preptime'].mean())

            # Verify if the computed values match the values in the dataframe
            self.assertEqual(row['xhist_avg_estimated_preptime'], avg_estimated_preptime)
            self.assertEqual(row['xhist_avg_actual_preptime'], avg_actual_preptime)


# Run the unit tests
if __name__ == '__main__':
    unittest.main()
