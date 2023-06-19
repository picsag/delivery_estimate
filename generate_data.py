import pandas as pd


def read_data(path: str, drop_nan: bool = True) -> pd.DataFrame:
    data = pd.read_csv(path, encoding='utf-8')
    data = data.replace('', None)

    print("=== Number of None values ===")
    print(data.isnull().sum())

    data = data.astype(pd.Int32Dtype())

    if drop_nan:
        data = data.dropna()

    # data.to_csv("./data/data_final.csv", index=False)

    print(data.head())
    print("=== Number of None values ===")
    print(data.isnull().sum())

    print(data.describe())

    data.info()

    return data


def train_gan(data: pd.DataFrame = None, save_data: bool = False,
                file_path: str = None, artifact_file: str = None) -> None:
    assert data is not None

    # trains the GAN on the final dataset


def generate_data(artifact: str = None, length: int = 1000,
                  save_data: bool = False, file_path: str = None) -> pd.DataFrame:
    # generates artifical data . . .

    if save_data:
        data.to_csv(file_path, index=False)

    return data


if __name__ == "__main__":
    training = True
    artifact_file = "./data/GAN_delivery.pkl"

    df = read_data(path="./data/data_final.csv", drop_nan=False)

    if training:
        train_gan(df, file_path="./data/data_final_artificial.csv", save_data=True, artifact_file=artifact_file)
    else:
        sample_data = generate_data(artifact=artifact_file, length=len(df))
        print(sample_data)
