# Purpose: Calculate portfolio covariance matrix, variance, and summary metrics.

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def normalize_weights(weights: Iterable[float]) -> np.ndarray:
    """Normalize portfolio weights so that they sum to 1.

    Args:
        weights: Iterable of asset weights.

    Returns:
        Normalized numpy array of weights.
    """
    weight_array = np.asarray(list(weights), dtype=float)
    total = weight_array.sum()
    if weight_array.size == 0 or np.isclose(total, 0.0):
        raise ValueError("Weights must be non-empty and sum to a non-zero value.")
    return weight_array / total


def calculate_covariance_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate covariance matrix from returns.

    Args:
        returns_df: DataFrame of daily log returns.

    Returns:
        Covariance matrix DataFrame.
    """
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty. Cannot compute covariance.")
    return returns_df.cov()


def calculate_portfolio_variance(cov_matrix: pd.DataFrame, weights: Iterable[float]) -> float:
    """Calculate portfolio variance using covariance matrix and weights.

    Args:
        cov_matrix: Covariance matrix of returns.
        weights: Portfolio weights.

    Returns:
        Portfolio variance as float.
    """
    normalized_weights = normalize_weights(weights)
    covariance_values = cov_matrix.to_numpy(dtype=float)
    return float(normalized_weights.T @ covariance_values @ normalized_weights)


def calculate_portfolio_volatility(cov_matrix: pd.DataFrame, weights: Iterable[float]) -> float:
    """Calculate portfolio daily volatility as standard deviation.

    Args:
        cov_matrix: Covariance matrix of returns.
        weights: Portfolio weights.

    Returns:
        Portfolio daily volatility.
    """
    variance = calculate_portfolio_variance(cov_matrix, weights)
    return float(np.sqrt(variance))


def build_portfolio_summary(
    returns_df: pd.DataFrame,
    cov_matrix: pd.DataFrame,
    weights: Iterable[float],
    trading_days: int = 252,
) -> pd.DataFrame:
    """Build a one-row portfolio summary table.

    Args:
        returns_df: DataFrame of daily log returns.
        cov_matrix: Covariance matrix of returns.
        weights: Portfolio weights.
        trading_days: Trading days used for annualization.

    Returns:
        Summary DataFrame with mean return, variance, and volatility metrics.
    """
    normalized_weights = normalize_weights(weights)
    mean_daily_return = float(np.dot(returns_df.mean().to_numpy(dtype=float), normalized_weights))
    portfolio_variance = calculate_portfolio_variance(cov_matrix, normalized_weights)
    daily_volatility = float(np.sqrt(portfolio_variance))

    summary = pd.DataFrame(
        {
            "mean_daily_log_return": [mean_daily_return],
            "annualized_log_return_estimate": [mean_daily_return * trading_days],
            "portfolio_variance_daily": [portfolio_variance],
            "portfolio_volatility_daily": [daily_volatility],
            "portfolio_volatility_annualized": [daily_volatility * np.sqrt(trading_days)],
        }
    )
    return summary


def save_dataframe(dataframe: pd.DataFrame, output_path: str) -> None:
    """Save a DataFrame to CSV.

    Args:
        dataframe: DataFrame to save.
        output_path: Destination CSV path.
    """
    dataframe.to_csv(output_path, index=True)

