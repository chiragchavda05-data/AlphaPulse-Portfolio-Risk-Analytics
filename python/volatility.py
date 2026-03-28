# Purpose: Compute rolling 30-day volatility metrics from daily log returns.

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from portfolio_metrics import normalize_weights


def calculate_rolling_volatility(
    returns_df: pd.DataFrame,
    window: int = 30,
    annualize: bool = True,
    trading_days: int = 252,
) -> pd.DataFrame:
    """Calculate rolling volatility for each asset.

    Args:
        returns_df: Daily log returns DataFrame.
        window: Rolling window size in days.
        annualize: Whether to annualize volatility values.
        trading_days: Trading days for annualization.

    Returns:
        DataFrame with rolling volatility per asset.
    """
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty. Cannot compute volatility.")
    if window < 2:
        raise ValueError("Rolling window must be at least 2.")

    rolling_std = returns_df.rolling(window=window).std()
    if annualize:
        rolling_std = rolling_std * np.sqrt(trading_days)

    rolling_std.index.name = "Date"
    return rolling_std.dropna(how="all")


def calculate_portfolio_daily_returns(returns_df: pd.DataFrame, weights: Iterable[float]) -> pd.Series:
    """Compute daily portfolio log returns from asset returns and weights.

    Args:
        returns_df: Daily log returns DataFrame.
        weights: Portfolio weights aligned to returns_df columns.

    Returns:
        Series of daily portfolio log returns.
    """
    normalized_weights = normalize_weights(weights)
    if returns_df.shape[1] != normalized_weights.size:
        raise ValueError("Number of weights must match number of assets.")

    portfolio_returns = returns_df.to_numpy(dtype=float) @ normalized_weights
    return pd.Series(portfolio_returns, index=returns_df.index, name="portfolio_log_return")


def calculate_portfolio_rolling_volatility(
    returns_df: pd.DataFrame,
    weights: Iterable[float],
    window: int = 30,
    annualize: bool = True,
    trading_days: int = 252,
) -> pd.DataFrame:
    """Compute rolling volatility for portfolio returns.

    Args:
        returns_df: Daily log returns DataFrame.
        weights: Portfolio weights aligned to returns_df columns.
        window: Rolling window size in days.
        annualize: Whether to annualize volatility values.
        trading_days: Trading days for annualization.

    Returns:
        DataFrame with Date index and portfolio rolling volatility.
    """
    portfolio_returns = calculate_portfolio_daily_returns(returns_df, weights)
    rolling_vol = portfolio_returns.rolling(window=window).std()
    if annualize:
        rolling_vol = rolling_vol * np.sqrt(trading_days)

    output = rolling_vol.to_frame(name=f"portfolio_rolling_vol_{window}d")
    output.index.name = "Date"
    return output.dropna(how="all")


def save_volatility(dataframe: pd.DataFrame, output_path: str) -> None:
    """Save volatility DataFrame to CSV.

    Args:
        dataframe: Volatility DataFrame.
        output_path: Destination CSV path.
    """
    dataframe.to_csv(output_path)

