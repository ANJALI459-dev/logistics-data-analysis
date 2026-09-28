"""
Week 2 - Logistics Data Collection, Cleaning and Preprocessing
Reference dataset: DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS.
This script can run on the supplied illustrative CSV, or on a downloaded
DataCoSupplyChainDataset.csv after changing INPUT_FILE.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

INPUT_FILE = Path("logistics_sample_dirty.csv")
OUTPUT_FILE = Path("logistics_cleaned.csv")

# 1. Load data
df = pd.read_csv(INPUT_FILE)
print("Raw shape:", df.shape)

# 2. Standardize column names
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(r"[^a-z0-9]+", "_", regex=True)
              .str.strip("_")
)

# 3. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print("Duplicates removed:", before - len(df))

# 4. Parse dates and enforce numeric types
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

numeric_cols = [
    "days_for_shipping_real",
    "days_for_shipment_scheduled",
    "order_item_quantity",
    "sales",
    "order_item_discount_rate",
    "late_delivery_risk",
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. Missing-value treatment
# Median is used for skewed/continuous numeric variables so extreme values
# do not dominate the imputation. Mode is used for categorical variables.
for col in ["sales", "order_item_quantity"]:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

if "shipping_mode" in df.columns:
    df["shipping_mode"] = df["shipping_mode"].fillna(df["shipping_mode"].mode()[0])

# 6. Outlier treatment using IQR capping for sales
if "sales" in df.columns:
    q1 = df["sales"].quantile(0.25)
    q3 = df["sales"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    df["sales"] = df["sales"].clip(lower=lower, upper=upper)

# 7. Logical validation
if {"days_for_shipping_real", "days_for_shipment_scheduled"}.issubset(df.columns):
    df["delivery_delay_days"] = (
        df["days_for_shipping_real"] - df["days_for_shipment_scheduled"]
    )
    df["late_delivery_risk"] = (df["delivery_delay_days"] > 0).astype(int)

# 8. Min-max normalization for selected continuous variables
scale_cols = [
    c for c in ["sales", "order_item_quantity", "order_item_discount_rate"]
    if c in df.columns
]
if scale_cols:
    scaler = MinMaxScaler()
    df[[f"{c}_normalized" for c in scale_cols]] = scaler.fit_transform(df[scale_cols])

# 9. Final quality checks
print("\nMissing values after cleaning:")
print(df.isna().sum())
print("\nDuplicate rows after cleaning:", df.duplicated().sum())
print("\nCleaned shape:", df.shape)

df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved cleaned dataset to: {OUTPUT_FILE}")
