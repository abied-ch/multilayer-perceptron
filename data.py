import pandas as pd
import numpy as np
from numpy import ndarray

class Data:
    def __init__(self, csv_path: str, drop_columns: list[str] = None) -> None:
        # The data is missing headers, header=None prevents pandas from interpreting
        # the first row as column names
        self.df = pd.read_csv(csv_path, header=None)
        self._preprocess(drop_columns)

    def _preprocess(self, drop_columns: list[str]) -> None:
        # Temporarily add the columns for easier preprocessing
        self._add_columns()

        # Remove irrelevant columns
        if drop_columns:
            self.df.drop(drop_columns, axis=1, inplace=True)

        # Convert categorical data into numerical for loss calculation
        self.df["diagnosis"] = self.df["diagnosis"].map({"M": 1, "B": 0})

        # Fill missing values with mean for their column to ensure
        # they have no impact on the dataset
        self.df = self.df.fillna(self.df.mean())

        # Scale features for faster convergence
        for column in self.df.columns:
            if column != "diagnosis":
                self.df[column] = (self.df[column] - self.df[column].mean()) / self.df[column].std()

        # Check shapes before conversion
        print("DataFrame shape after preprocessing:", self.df.shape)

        # Separate the input from the target values and convert them to NumPy arrays
        self.X = self.df.drop("diagnosis", axis=1).to_numpy()
        self.y = self.df["diagnosis"].to_numpy().reshape(-1, 1)

        # Check shapes after conversion
        print("Shape of X:", self.X.shape)
        print("Shape of y:", self.y.shape)

    def _add_columns(self) -> None:
        columns = [
            "id",
            "diagnosis",
            "radius_mean",
            "texture_mean",
            "perimeter_mean",
            "area_mean",
            "smoothness_mean",
            "compactness_mean",
            "concavity_mean",
            "concave points_mean",
            "symmetry_mean",
            "fractal_dimension_mean",
            "radius_se",
            "texture_se",
            "perimeter_se",
            "area_se",
            "smoothness_se",
            "compactness_se",
            "concavity_se",
            "concave points_se",
            "symmetry_se",
            "fractal_dimension_se",
            "radius_worst",
            "texture_worst",
            "perimeter_worst",
            "area_worst",
            "smoothness_worst",
            "compactness_worst",
            "concavity_worst",
            "concave points_worst",
            "symmetry_worst",
            "fractal_dimension_worst",
        ]

        self.df.columns = columns

def train_test_split(x: ndarray, y: ndarray, split: float) -> tuple:
    assert 0 < split < 1, "Split ratio must be between 0 and 1."

    indices = np.arange(x.shape[0])
    np.random.shuffle(indices)

    x_shuffled = x[indices]
    y_shuffled = y[indices]

    split_idx = int(x.shape[0] * (1 - split))

    x_train = x_shuffled[:split_idx]
    y_train = y_shuffled[:split_idx]
    x_test = x_shuffled[split_idx:]
    y_test = y_shuffled[split_idx:]

    return x_train, y_train, x_test, y_test
