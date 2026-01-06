from typing import List, Tuple
import yfinance as yf


def _scalar(value):
    """
    Safely extract a scalar from a pandas value or return the value itself.
    This avoids FutureWarning when yfinance returns single-element Series.
    """
    return value.iloc[0] if hasattr(value, "iloc") else value


def fetch_ohlcv(ticker: str, interval: str) -> List[Tuple]:
    """
    Fetch OHLCV data for a given ticker from Yahoo Finance.

    Returns:
        List of tuples in the format:
        (ticker, timestamp, open, high, low, close, volume)
    """
    ticker = ticker.upper().strip()

    data = yf.download(
        ticker,
        interval=interval,
        progress=False,
        auto_adjust=False,
        threads=False,
    )

    if data.empty:
        return []

    data = data.dropna()

    rows: List[Tuple] = []

    for timestamp, row in data.iterrows():
        open_ = float(_scalar(row["Open"]))
        high = float(_scalar(row["High"]))
        low = float(_scalar(row["Low"]))
        close = float(_scalar(row["Close"]))
        volume = int(_scalar(row["Volume"]))

        # Basic OHLC sanity check
        if high < low:
            continue

        rows.append(
            (
                ticker,
                timestamp.isoformat(),
                open_,
                high,
                low,
                close,
                volume,
            )
        )

    return rows
