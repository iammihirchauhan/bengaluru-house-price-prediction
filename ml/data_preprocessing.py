
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Bengaluru_House_Data.csv"


def convert_sqft(value):
    """Convert supported area values into square feet."""
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    # Handle ranges such as 1000 - 1200
    if "-" in value:
        parts = value.split("-")
        try:
            return (float(parts[0]) + float(parts[1])) / 2
        except ValueError:
            return np.nan

    # Handle different area units
    conversions = {
        "Sq. Meter": 10.7639,
        "Sq. Yards": 9,
        "Acres": 43560,
        "Cents": 435.6,
        "Guntha": 1089,
        "Grounds": 2400,
        "Sq. Feet": 1,
        "Perch": 272.25,
    }

    for unit, factor in conversions.items():
        if unit in value:
            try:
                number = float(value.replace(unit, "").strip())
                return number * factor
            except ValueError:
                return np.nan

    try:
        return float(value)
    except ValueError:
        return np.nan


def clean_data():
    df = pd.read_csv(DATA_PATH)

    # Remove duplicate records
    df = df.drop_duplicates().copy()

    # Remove rows without essential information
    df = df.dropna(subset=["location", "size", "total_sqft", "price"])

    # Clean location
    df["location"] = df["location"].str.strip()

    # Extract BHK count
    df["bhk"] = df["size"].str.extract(r"(\d+)").astype(int)

    # Convert square feet
    df["total_sqft"] = df["total_sqft"].apply(convert_sqft)

    # Remove rows where conversion failed
    df = df.dropna(subset=["total_sqft"])

    # Fill missing numeric values
    df["bath"] = df["bath"].fillna(df["bath"].median())
    df["balcony"] = df["balcony"].fillna(df["balcony"].median())

    # Remove columns not used in the initial model
    df = df.drop(columns=["society", "availability", "size"])

    # Remove impossible values
    df = df[
        (df["total_sqft"] > 0) &
        (df["price"] > 0) &
        (df["bhk"] > 0) &
        (df["bath"] > 0)
    ].copy()

    return df


if __name__ == "__main__":
    cleaned_df = clean_data()

    print("Original dataset: 13,320 rows")
    print("Cleaned dataset:", cleaned_df.shape)
    print("\nMissing values:")
    print(cleaned_df.isnull().sum())
    print("\nFirst five rows:")
    print(cleaned_df.head())

    output_path = BASE_DIR / "data" / "cleaned_bengaluru.csv"
    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved:", output_path)
