
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "cleaned_bengaluru.csv"

df = pd.read_csv(DATA_PATH)

# Price is stored in lakhs. Convert to rupees per square foot.
df["price_per_sqft"] = (df["price"] * 100000) / df["total_sqft"]

# Area available per bedroom
df["sqft_per_bhk"] = df["total_sqft"] / df["bhk"]

print("DATASET SHAPE:", df.shape)

print("\n1. PRICE PER SQFT STATISTICS")
print(df["price_per_sqft"].describe(
    percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
))

print("\n2. AREA PER BHK STATISTICS")
print(df["sqft_per_bhk"].describe())

print("\n3. PROPERTIES WITH LESS THAN 300 SQFT PER BHK")
print(df[df["sqft_per_bhk"] < 300].head(10))

print("\nCount:", (df["sqft_per_bhk"] < 300).sum())

print("\n4. PROPERTIES WITH MORE THAN 2000 SQFT PER BHK")
print(df[df["sqft_per_bhk"] > 2000].head(10))

print("\nCount:", (df["sqft_per_bhk"] > 2000).sum())

print("\n5. BATHROOMS GREATER THAN BHK + 2")
print(df[df["bath"] > df["bhk"] + 2].head(10))

print("\nCount:", (df["bath"] > df["bhk"] + 2).sum())

print("\n6. PRICE PER SQFT EXTREMES")
print("Lowest:", df["price_per_sqft"].min())
print("Highest:", df["price_per_sqft"].max())

print("\n7. TOP 10 LOCATIONS BY PROPERTY COUNT")
print(df["location"].value_counts().head(10))
