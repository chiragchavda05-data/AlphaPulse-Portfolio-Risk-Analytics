# Purpose: Compute and export daily log returns from cleaned price data.

from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_daily_log_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily log returns from adjusted close prices.

    Args:
        price_df: Cleaned adjusted close price DataFrame.

    Returns:
        DataFrame of daily log returns.
    """
    if price_df.empty:
        raise ValueError("Price DataFrame is empty. Cannot compute returns.")

    log_returns = np.log(price_df / price_df.shift(1)).dropna(how="any")
    log_returns.index.name = "Date"
    return log_returns


def save_returns(dataframe: pd.DataFrame, output_path: str) -> None:
    """Save log returns DataFrame to CSV.

    Args:
        dataframe: Log returns DataFrame.
        output_path: Destination CSV path.
    """
    dataframe.to_csv(output_path)

