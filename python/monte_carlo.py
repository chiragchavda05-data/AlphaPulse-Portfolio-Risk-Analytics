# Purpose: Run Monte Carlo portfolio simulations and compute 95% Value at Risk (VaR).

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np
import pandas as pd

from portfolio_metrics import normalize_weights


def simulate_portfolio_distribution(
    returns_df: pd.DataFrame,
    weights: Iterable[float],
    initial_value: float = 100000.0,
    simulations: int = 10000,
    days: int = 252,
    random_seed: int = 42,
) -> pd.DataFrame:
    """Run a Monte Carlo simulation for 1-year portfolio value distribution.

    Args:
        returns_df: Historical daily log returns by asset.
        weights: Portfolio weights.
        initial_value: Initial portfolio value.
        simulations: Number of Monte Carlo runs.
        days: Number of trading days to simulate.
        random_seed: Random seed for reproducibility.

    Returns:
        DataFrame with terminal values and returns for each simulation.
    """
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty. Cannot run simulation.")
    if simulations < 1:
        raise ValueError("Simulations must be at least 1.")
    if days < 1:
        raise ValueError("Days must be at least 1.")

    normalized_weights = normalize_weights(weights)
    if returns_df.shape[1] != normalized_weights.size:
        raise ValueError("Number of weights must match number of assets.")

    mean_vector = returns_df.mean().to_numpy(dtype=float)
    cov_matrix = returns_df.cov().to_numpy(dtype=float)

    rng = np.random.default_rng(random_seed)
    simulated_asset_returns = rng.multivariate_normal(
        mean=mean_vector,
        cov=cov_matrix,
        size=(simulations, days),
        check_valid="warn",
    )

    portfolio_daily_log_returns = np.tensordot(simulated_asset_returns, normalized_weights, axes=([2], [0]))
    cumulative_log_returns = portfolio_daily_log_returns.sum(axis=1)
    terminal_values = initial_value * np.exp(cumulative_log_returns)
    terminal_returns = (terminal_values / initial_value) - 1.0

    distribution_df = pd.DataFrame(
        {
            "simulation_id": np.arange(1, simulations + 1),
            "terminal_value": terminal_values,
            "terminal_return": terminal_returns,
        }
    )
    return distribution_df


def calculate_var_95(distribution_df: pd.DataFrame, initial_value: float = 100000.0) -> Tuple[float, float]:
    """Calculate 95% one-year Value at Risk from Monte Carlo terminal distribution.

    Args:
        distribution_df: DataFrame returned by simulate_portfolio_distribution.
        initial_value: Initial portfolio value.

    Returns:
        Tuple of (VaR amount in currency, VaR as percentage of initial value).
    """
    if distribution_df.empty or "terminal_value" not in distribution_df.columns:
        raise ValueError("Distribution data must include terminal_value.")

    terminal_values = distribution_df["terminal_value"].to_numpy(dtype=float)
    value_at_5th_percentile = float(np.percentile(terminal_values, 5))
    var_amount = max(0.0, initial_value - value_at_5th_percentile)
    var_percent = var_amount / initial_value
    return var_amount, var_percent


def save_distribution(dataframe: pd.DataFrame, output_path: str) -> None:
    """Save Monte Carlo distribution to CSV.

    Args:
        dataframe: Monte Carlo result DataFrame.
        output_path: Destination CSV path.
    """
    dataframe.to_csv(output_path, index=False)

