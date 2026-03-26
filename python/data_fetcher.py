# Purpose: Fetch historical adjusted close price data using yfinance and persist raw data to CSV.

from __future__ import annotations

from typing import Iterable, List

import pandas as pd
import yfinance as yf


def fetch_adjusted_close_prices(
    tickers: Iterable[str],
    start_date: str,
    end_date: str,
    interval: str = "1d",
) -> pd.DataFrame:
    """Fetch adjusted close prices for the provided tickers and date range.

    Args:
        tickers: Iterable of ticker symbols (e.g., ["AAPL", "MSFT"]).
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
        interval: Data interval supported by yfinance (default: "1d").

    Returns:
        DataFrame indexed by date with one column per ticker.

    Raises:
        RuntimeError: If yfinance fails or returns no usable adjusted close data.
    """
    symbols: List[str] = [ticker.strip().upper() for ticker in tickers if str(ticker).strip()]
    if not symbols:
        raise ValueError("At least one valid ticker symbol is required.")

    try:
        data = yf.download(
            tickers=symbols,
            start=start_date,
            end=end_date,
            interval=interval,
            auto_adjust=False,
            progress=False,
            group_by="column",
            threads=True,
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch data from yfinance: {exc}") from exc

    if data.empty:
        raise RuntimeError("yfinance returned an empty dataset.")

    if len(symbols) == 1:
        adjusted_close = data.get("Adj Close")
        if adjusted_close is None:
            adjusted_close = data.get("Close")
        if adjusted_close is None:
            raise RuntimeError("Adjusted close data is not available for the provided ticker.")
        adjusted_close = adjusted_close.to_frame(name=symbols[0])
    else:
        if "Adj Close" in data.columns.get_level_values(0):
            adjusted_close = data["Adj Close"].copy()
        elif "Close" in data.columns.get_level_values(0):
            adjusted_close = data["Close"].copy()
        else:
            raise RuntimeError("Adjusted close data is not available for one or more tickers.")

    adjusted_close.index = pd.to_datetime(adjusted_close.index)
    adjusted_close = adjusted_close.sort_index()
    adjusted_close.columns = [str(col).upper() for col in adjusted_close.columns]
    adjusted_close.index.name = "Date"

    if adjusted_close.empty:
        raise RuntimeError("No adjusted close data available after processing.")

    return adjusted_close


def save_raw_data(dataframe: pd.DataFrame, output_path: str) -> None:
    """Save raw adjusted close price data to CSV.

    Args:
        dataframe: Price DataFrame indexed by date.
        output_path: Destination CSV path.
    """
    dataframe.to_csv(output_path)

