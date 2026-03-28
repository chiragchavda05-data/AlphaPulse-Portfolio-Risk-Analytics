# Purpose: Build correlation matrix and export data shaped for heatmap visualization.

from __future__ import annotations

import pandas as pd


def calculate_correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Pearson correlation matrix of asset returns.

    Args:
        returns_df: DataFrame of daily log returns.

    Returns:
        Correlation matrix DataFrame.
    """
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty. Cannot compute correlation.")
    return returns_df.corr()


def export_heatmap_data(correlation_df: pd.DataFrame) -> pd.DataFrame:
    """Convert correlation matrix to long format suitable for heatmap plotting.

    Args:
        correlation_df: Square correlation matrix DataFrame.

    Returns:
        Long-form DataFrame with asset pairs and correlation value.
    """
    if correlation_df.empty:
        raise ValueError("Correlation DataFrame is empty. Cannot export heatmap data.")

    heatmap_data = (
        correlation_df.reset_index()
        .melt(id_vars="index", var_name="asset_y", value_name="correlation")
        .rename(columns={"index": "asset_x"})
    )
    return heatmap_data


def save_dataframe(dataframe: pd.DataFrame, output_path: str, index: bool = True) -> None:
    """Save a DataFrame to CSV.

    Args:
        dataframe: DataFrame to save.
        output_path: Destination CSV path.
        index: Whether to include index in CSV.
    """
    dataframe.to_csv(output_path, index=index)

