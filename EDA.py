import pandas as pd


class ClusterAnalysis:
    def __init__(self, file_path):
        self.cluster_data = pd.read_csv(file_path)

    def compute_statistics(self):
        # Compute statistics for actual_preptime and estimated_preptime
        statistics = self.cluster_data.groupby('account_cluster_id').agg({
            'actual_preptime': ['mean', 'median', 'std', 'min', 'max'],
            'estimated_preptime': ['mean', 'median', 'std', 'min', 'max']
        })

        return statistics

    # Extend the class with additional capabilities for each cluster as needed


file_path = './data/data_final.csv'
cluster_analysis = ClusterAnalysis(file_path)
statistics = cluster_analysis.compute_statistics()
print(statistics)
