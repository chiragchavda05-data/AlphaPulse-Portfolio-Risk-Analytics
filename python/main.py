# Purpose: Orchestrate the AlphaPulse workflow from data fetch to portfolio risk output CSVs.

from __future__ import annotations

import os
from datetime import date, timedelta
from typing import List

import numpy as np
import pandas as pd

from correlation import calculate_correlation_matrix, export_heatmap_data, save_dataframe as save_correlation_df
from data_cleaner import clean_price_data, save_cleaned_data
from data_fetcher import fetch_adjusted_close_prices, save_raw_data
from monte_carlo import calculate_var_95, save_distribution, simulate_portfolio_distribution
from portfolio_metrics import (
    build_portfolio_summary,
    calculate_covariance_matrix,
    normalize_weights,
    save_dataframe as save_portfolio_df,
)
from returns_calculator import calculate_daily_log_returns, save_returns
from volatility import (
    calculate_portfolio_rolling_volatility,
    calculate_rolling_volatility,
    save_volatility,
)


def ensure_directories(base_dir: str) -> None:
    """Create required project directories if they do not already exist.

    Args:
        base_dir: Root project directory.
    """
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "output"), exist_ok=True)


def get_default_config() -> dict:
    """Build default runtime configuration for the AlphaPulse pipeline.

    Returns:
        Dictionary containing tickers, dates, portfolio settings, and simulation parameters.
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=365 * 5)
    tickers: List[str] = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    equal_weights = normalize_weights(np.ones(len(tickers)))

    return {
        "tickers": tickers,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "weights": equal_weights,
        "initial_portfolio_value": 100000.0,
        "simulation_runs": 10000,
        "simulation_days": 252,
        "rolling_window": 30,
    }


def run_pipeline(base_dir: str) -> None:
    """Execute the full AlphaPulse workflow and export all required CSV outputs.

    Args:
        base_dir: Root directory of the project.
    """
    ensure_directories(base_dir)
    config = get_default_config()

    data_dir = os.path.join(base_dir, "data")
    outputs_dir = os.path.join(base_dir, "output")

    raw_data_path = os.path.join(data_dir, "raw_data.csv")
    cleaned_data_path = os.path.join(data_dir, "cleaned_data.csv")
    returns_path = os.path.join(outputs_dir, "daily_log_returns.csv")
    covariance_path = os.path.join(outputs_dir, "covariance_matrix.csv")
    portfolio_summary_path = os.path.join(outputs_dir, "portfolio_summary.csv")
    monte_carlo_path = os.path.join(outputs_dir, "monte_carlo_terminal_distribution.csv")
    var_path = os.path.join(outputs_dir, "var_95.csv")
    asset_vol_path = os.path.join(outputs_dir, "rolling_30d_volatility_assets.csv")
    portfolio_vol_path = os.path.join(outputs_dir, "rolling_30d_volatility_portfolio.csv")
    correlation_path = os.path.join(outputs_dir, "correlation_matrix.csv")
    heatmap_data_path = os.path.join(outputs_dir, "correlation_heatmap_data.csv")

    print("[1/8] Fetching adjusted close price data from yfinance...")
    prices = fetch_adjusted_close_prices(
        tickers=config["tickers"],
        start_date=config["start_date"],
        end_date=config["end_date"],
    )
    save_raw_data(prices, raw_data_path)
    print(f"Saved raw data: {raw_data_path}")

    print("[2/8] Cleaning price data...")
    cleaned_prices = clean_price_data(prices)
    save_cleaned_data(cleaned_prices, cleaned_data_path)
    print(f"Saved cleaned data: {cleaned_data_path}")

    print("[3/8] Calculating daily log returns...")
    log_returns = calculate_daily_log_returns(cleaned_prices)
    save_returns(log_returns, returns_path)
    print(f"Saved daily log returns: {returns_path}")

    # Re-align weights in case one or more tickers were dropped during cleaning.
    configured_tickers = [ticker.upper() for ticker in config["tickers"]]
    weight_lookup = dict(zip(configured_tickers, config["weights"]))
    active_tickers = list(log_returns.columns)
    missing_tickers = sorted(set(configured_tickers) - set(active_tickers))
    if missing_tickers:
        print(f"Warning: Dropped tickers due to missing data: {', '.join(missing_tickers)}")
    active_weights = normalize_weights([weight_lookup[ticker] for ticker in active_tickers])

    print("[4/8] Calculating covariance matrix and portfolio metrics...")
    covariance_matrix = calculate_covariance_matrix(log_returns)
    save_portfolio_df(covariance_matrix, covariance_path)

    portfolio_summary = build_portfolio_summary(log_returns, covariance_matrix, active_weights)
    portfolio_summary.to_csv(portfolio_summary_path, index=False)
    print(f"Saved covariance matrix: {covariance_path}")
    print(f"Saved portfolio summary: {portfolio_summary_path}")

    print("[5/8] Running Monte Carlo simulation (10,000 runs, 1 year)...")
    simulation_df = simulate_portfolio_distribution(
        returns_df=log_returns,
        weights=active_weights,
        initial_value=config["initial_portfolio_value"],
        simulations=config["simulation_runs"],
        days=config["simulation_days"],
    )
    save_distribution(simulation_df, monte_carlo_path)
    print(f"Saved Monte Carlo terminal distribution: {monte_carlo_path}")

    var_amount, var_percent = calculate_var_95(
        distribution_df=simulation_df,
        initial_value=config["initial_portfolio_value"],
    )
    var_df = pd.DataFrame(
        {
            "confidence_level": [0.95],
            "initial_portfolio_value": [config["initial_portfolio_value"]],
            "var_95_amount": [var_amount],
            "var_95_percent": [var_percent],
        }
    )
    var_df.to_csv(var_path, index=False)
    print(f"Saved VaR 95% result: {var_path}")

    print("[6/8] Calculating rolling 30-day volatility...")
    asset_rolling_vol = calculate_rolling_volatility(log_returns, window=config["rolling_window"])
    save_volatility(asset_rolling_vol, asset_vol_path)

    portfolio_rolling_vol = calculate_portfolio_rolling_volatility(
        returns_df=log_returns,
        weights=active_weights,
        window=config["rolling_window"],
    )
    save_volatility(portfolio_rolling_vol, portfolio_vol_path)
    print(f"Saved rolling asset volatility: {asset_vol_path}")
    print(f"Saved rolling portfolio volatility: {portfolio_vol_path}")

    print("[7/8] Calculating correlation matrix and heatmap export data...")
    correlation_matrix = calculate_correlation_matrix(log_returns)
    save_correlation_df(correlation_matrix, correlation_path, index=True)

    heatmap_data = export_heatmap_data(correlation_matrix)
    save_correlation_df(heatmap_data, heatmap_data_path, index=False)
    print(f"Saved correlation matrix: {correlation_path}")
    print(f"Saved heatmap data: {heatmap_data_path}")

    print("[8/8] AlphaPulse workflow completed successfully.")


if __name__ == "__main__":
    # VS Code Terminal Example:
    #   python python/main.py
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        run_pipeline(project_root)
    except Exception as err:
        print(f"Pipeline failed: {err}")
        raise
