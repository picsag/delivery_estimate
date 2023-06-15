import pandas as pd


def extract_datetime_features(data):
    # Convert the 'added' column to datetime
    data['added'] = pd.to_datetime(data['added'])

    # Extract day of the week (Monday=0, Sunday=6)
    data['day_of_week'] = data['added'].dt.dayofweek

    # Extract weekend binary feature (1=Weekend, 0=Weekday)
    data['weekend'] = data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

    # Extract hour of the day
    data['hour_of_day'] = data['added'].dt.hour

    # Drop the original 'added' column
    data = data.drop('added', axis=1)

    return data


def main():
    # Read the CSV file
    data = pd.read_csv('./data/data_preprocessed.csv')

    # Remove the order_id column
    data = data.drop('order_id', axis=1)
    data = data.drop('account_id', axis=1)

    # Extract datetime features
    data = extract_datetime_features(data)
    data.to_csv('./data/data_final.csv', index=False)


if __name__ == '__main__':
    main()
