import pandas as pd
import numpy as np
import os

BASE_PATH = "data/processed"
os.makedirs(BASE_PATH, exist_ok=True)


def clean_dataset():
    # Load dataset
    df = pd.read_csv("data/raw/earthquake_5years_combined.csv")

    # --------------------------------------------------
    # Remove duplicate earthquake records
    # --------------------------------------------------
    if "id" in df.columns:
        df.drop_duplicates(subset=["id"], inplace=True)

    # --------------------------------------------------
    # Convert timestamps
    # --------------------------------------------------
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")

    if "updated" in df.columns:
        df["updated"] = pd.to_datetime(df["updated"], unit="ms", errors="coerce")

    # --------------------------------------------------
    # Extract Country from Place
    # Example:
    # "139 km ENE of Masohi, Indonesia"
    # ==> Indonesia
    # --------------------------------------------------
    if "place" in df.columns:
        df["country"] = (
            df["place"]
            .astype(str)
            .str.extract(r",\s*([^,]+)$")[0]
            .fillna("NaN")
            .str.strip()
        )

    # --------------------------------------------------
    # Numeric Column Standardization
    # --------------------------------------------------
    numeric_cols = [
        "depth_km",
        "latitude",
        "longitude",
        "mag",
        "felt",
        "cdi",
        "mmi",
        "nst",
        "dmin",
        "rms",
        "gap",
        "magError",
        "depthError",
        "magNst",
        "sig"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # --------------------------------------------------
    # Fill numeric missing values with mean
    # --------------------------------------------------
    fill_mean_cols = [
        "mag",
        "depth_km",
        "felt",
        "cdi",
        "mmi",
        "nst",
        "dmin",
        "rms",
        "gap",
        "magError",
        "depthError",
        "magNst"
    ]

    for col in fill_mean_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    # --------------------------------------------------
    # Validations
    # --------------------------------------------------

    # Depth must be positive
    if "depth_km" in df.columns:
        df["depth_km"] = df["depth_km"].abs()

    # Latitude must be between -90 and 90
    if "latitude" in df.columns:
        df["latitude"] = df["latitude"].clip(-90, 90)

    # Longitude must be between -180 and 180
    if "longitude" in df.columns:
        df["longitude"] = df["longitude"].clip(-180, 180)

    # Magnitude cannot be negative
    if "mag" in df.columns:
        df["mag"] = df["mag"].clip(lower=0)

    # Significance cannot be negative
    if "sig" in df.columns:
        df["sig"] = df["sig"].clip(lower=0)

    # Tsunami must be either 0 or 1
    if "tsunami" in df.columns:
        df["tsunami"] = (
            pd.to_numeric(df["tsunami"], errors="coerce")
            .fillna(0)
            .apply(lambda x: 1 if x == 1 else 0)
        )

    # --------------------------------------------------
    # Alert Cleaning
    # --------------------------------------------------
    if "alert" in df.columns:
        df["alert"] = (
            df["alert"]
            .replace(r"^\s*$", "NaN", regex=True)
            .fillna("NaN")
            .astype(str)
            .str.lower()
            .str.strip()
        )

    # --------------------------------------------------
    # Text Columns Cleaning
    # --------------------------------------------------
    text_cols = [
        "magType",
        "status",
        "type",
        "net",
        "sources",
        "types",
        "ids",
        "locationSource",
        "magSource"
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .fillna("NaN")
                .astype(str)
                .str.strip()
                .str.lower()
                .str.replace(r"^,+|,+$", "", regex=True)
            )

    # --------------------------------------------------
    # Date Features
    # --------------------------------------------------
    if "time" in df.columns:
        df["year"] = df["time"].dt.year
        df["month"] = df["time"].dt.month
        df["day"] = df["time"].dt.day
        df["hour"] = df["time"].dt.hour
        df["day_of_week"] = df["time"].dt.day_name()

    # --------------------------------------------------
    # Depth Classification
    # --------------------------------------------------
    if "depth_km" in df.columns:
        df["depth_category"] = pd.cut(
            df["depth_km"],
            bins=[-float("inf"), 70, 300, float("inf")],
            labels=[
                "shallow",
                "intermediate",
                "deep"
            ]
        )

    # --------------------------------------------------
    # Magnitude Classification
    # --------------------------------------------------
    if "mag" in df.columns:
        df["magnitude_flag"] = np.select(
            [
                df["mag"] >= 7.0,
                df["mag"] >= 6.0
            ],
            [
                "destructive",
                "strong"
            ],
            default="normal"
        )

    # --------------------------------------------------
    # Validate Updated Timestamp
    # --------------------------------------------------
    if {"time", "updated"}.issubset(df.columns):
        invalid_dates = df["updated"] < df["time"]

        if invalid_dates.any():
            df.loc[invalid_dates, "updated"] = df.loc[
                invalid_dates,
                "time"
            ]

    # --------------------------------------------------
    # Standardize magType
    # --------------------------------------------------
    if "magType" in df.columns:
        df["magType"] = (
            df["magType"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

    # --------------------------------------------------
    # Save Processed Dataset
    # --------------------------------------------------
    output_file = os.path.join(
        BASE_PATH,
        "global_table.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"Cleaning completed.")
    print(f"Saved to: {output_file}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    clean_dataset()