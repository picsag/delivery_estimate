import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from tqdm import tqdm


def split_data(data, cluster_column, test_size=0.25, random_state=42):
    # Set random seed for reproducibility
    np.random.seed(random_state)

    train_data = pd.DataFrame()
    test_data = pd.DataFrame()

    # Group data by cluster_column
    grouped = data.groupby(cluster_column)

    for _, group in grouped:
        # Split data into train and test sets based on the specified test_size
        train_group, test_group = train_test_split(group, test_size=test_size)

        # Concatenate train and test sets to respective dataframes
        train_data = pd.concat([train_data, train_group])
        test_data = pd.concat([test_data, test_group])

    return train_data, test_data


class RandomForestTrainer:
    def __init__(self, train_data, test_data, cluster_column):
        self.train_data = train_data
        self.test_data = test_data
        self.cluster_column = cluster_column
        self.models = {}

    def train_models(self):
        clusters = self.train_data[self.cluster_column].unique()

        for cluster in tqdm(clusters, desc="Training models"):
            # Filter data for the current cluster
            cluster_data = self.train_data[self.train_data[self.cluster_column] == cluster]

            # Separate features and target variable
            X_train = cluster_data.drop('actual_preptime', axis=1)
            y_train = cluster_data['actual_preptime']

            # Train a RandomForestRegressor
            model = RandomForestRegressor()
            model.fit(X_train, y_train)

            # Save the model to a pickle file
            cluster_id = int(cluster)  # Extract the integer part of the cluster_id
            filename = f'./models/randomforest_{cluster_id}.pickle'
            with open(filename, 'wb') as file:
                pickle.dump(model, file)

            self.models[cluster] = filename

    def load_and_test_models(self, mse_filename):
        mse_scores = []

        for cluster, filename in self.models.items():
            # Load the model from the pickle file
            with open(filename, 'rb') as file:
                model = pickle.load(file)

            # Filter test data for the current cluster
            cluster_data = self.test_data[self.test_data[self.cluster_column] == cluster]

            # Separate features and target variable
            X_test = cluster_data.drop('actual_preptime', axis=1)
            y_test = cluster_data['actual_preptime']

            # Predict using the loaded model
            y_pred = model.predict(X_test)

            # Calculate Mean Squared Error (MSE)
            mse = mean_squared_error(y_test, y_pred)
            mse_scores.append({'account_cluster_id': cluster, 'mse_score': mse})

        # Save MSE scores to the CSV file
        mse_df = pd.DataFrame(mse_scores)
        mse_df.to_csv(mse_filename, index=False)


def main():
    # Read the CSV file
    data = pd.read_csv('./data/data_final.csv')

    # Split the data into train and test sets
    train_data, test_data = split_data(data, 'account_cluster_id')

    # Create an instance of the RandomForestTrainer class
    trainer = RandomForestTrainer(train_data, test_data, 'account_cluster_id')

    # Train the models and save them in pickle files
    trainer.train_models()

    # Specify the filename for MSE scores
    mse_filename = 'mse_scores_randomforest.csv'

    # Load the saved models, test them on the test data, and save MSE scores
    trainer.load_and_test_models(mse_filename)


if __name__ == '__main__':
    main()