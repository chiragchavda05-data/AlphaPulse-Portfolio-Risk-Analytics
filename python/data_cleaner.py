# Purpose: Clean raw stock price data for downstream risk and volatility analytics.

from __future__ import annotations

import pandas as pd


def clean_price_data(price_df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw price data by sorting dates, handling missing values, and filtering invalid rows.

    Args:
        price_df: Raw adjusted close price DataFrame indexed by date.

    Returns:
        Cleaned DataFrame ready for return calculations.
    """
    if price_df.empty:
        raise ValueError("Input price data is empty.")

    cleaned = price_df.copy()
    cleaned.index = pd.to_datetime(cleaned.index)
    cleaned = cleaned.sort_index()

    # Remove tickers that contain no data at all.
    cleaned = cleaned.dropna(axis=1, how="all")
    if cleaned.shape[1] == 0:
        raise ValueError("All ticker columns are empty after fetch. Please check symbols/date range.")

    # Fill gaps and then keep rows where all remaining tickers are valid.
    cleaned = cleaned.ffill().bfill().dropna(how="any")

    if cleaned.empty:
        raise ValueError("No valid data remains after cleaning.")

    cleaned.index.name = "Date"
    return cleaned


def save_cleaned_data(dataframe: pd.DataFrame, output_path: str) -> None:
    """Save cleaned price data to CSV.

    Args:
        dataframe: Cleaned price DataFrame.
        output_path: Destination CSV path.
    """
    dataframe.to_csv(output_path)
