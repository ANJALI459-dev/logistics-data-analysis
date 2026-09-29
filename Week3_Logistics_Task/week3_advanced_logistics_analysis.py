"""
Week 3 Task: Advanced Data Analysis and Visualization in Logistics
Synthetic dataset + EDA + visualizations.

This project uses a reproducible hypothetical logistics dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("week3_logistics_dataset.csv")

# Basic inspection
print(df.head())
print(df.info())
print(df.describe(include="all"))

# Missing-value check
print("\nMissing values:")
print(df.isna().sum())

# Cleaning: median imputation for numeric fields
numeric_cols = [
    "distance_km", "shipment_volume_kg", "warehouse_delay_days",
    "fuel_price_index", "delivery_time_days", "transport_cost_inr"
]
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# IQR-based outlier treatment using clipping
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    df[col] = df[col].clip(lower, upper)

# Descriptive statistics
print("\nDescriptive statistics:")
print(df[numeric_cols].describe())

# Correlation
print("\nCorrelation matrix:")
print(df[numeric_cols].corr())

# Visualization 1: delivery-time distribution
plt.figure(figsize=(8, 5))
plt.hist(df["delivery_time_days"], bins=18, edgecolor="black")
plt.xlabel("Delivery time (days)")
plt.ylabel("Number of orders")
plt.title("Distribution of Delivery Time")
plt.tight_layout()
plt.show()

# Visualization 2: shipment volume by route
route_vol = df.groupby("route_region")["shipment_volume_kg"].mean()
route_vol.plot(kind="bar", figsize=(8, 5))
plt.ylabel("Average shipment volume (kg)")
plt.title("Average Shipment Volume by Route Region")
plt.tight_layout()
plt.show()

# Visualization 3: distance vs cost
plt.figure(figsize=(8, 5))
plt.scatter(df["distance_km"], df["transport_cost_inr"], alpha=0.65)
plt.xlabel("Distance (km)")
plt.ylabel("Transport cost (INR)")
plt.title("Distance vs Transport Cost")
plt.tight_layout()
plt.show()

# Visualization 4: warehouse delay vs delivery time
plt.figure(figsize=(8, 5))
plt.scatter(df["warehouse_delay_days"], df["delivery_time_days"], alpha=0.65)
plt.xlabel("Warehouse delay (days)")
plt.ylabel("Delivery time (days)")
plt.title("Warehouse Delay vs Delivery Time")
plt.tight_layout()
plt.show()

# Visualization 5: average cost by carrier
carrier_cost = df.groupby("carrier")["transport_cost_inr"].mean().sort_values()
carrier_cost.plot(kind="bar", figsize=(8, 5))
plt.ylabel("Average transport cost (INR)")
plt.title("Average Transport Cost by Carrier")
plt.tight_layout()
plt.show()
