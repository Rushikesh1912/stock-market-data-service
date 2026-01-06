import pandas as pd
from unittest.mock import patch
from app.fetcher import fetch_ohlcv


@patch("app.fetcher.yf.download")
def test_fetch_ohlcv_valid_data(mock_download):
    # Arrange: mock Yahoo Finance response
    data = pd.DataFrame(
        {
            "Open": [100.0],
            "High": [110.0],
            "Low": [90.0],
            "Close": [105.0],
            "Volume": [1000],
        },
        index=[pd.Timestamp("2024-01-01")],
    )

    mock_download.return_value = data

    # Act
    rows = fetch_ohlcv("AAPL", "1d")

    # Assert
    assert len(rows) == 1
    assert rows[0][0] == "AAPL"
    assert rows[0][2] == 100.0
    assert rows[0][3] == 110.0
    assert rows[0][4] == 90.0
    assert rows[0][5] == 105.0
    assert rows[0][6] == 1000


@patch("app.fetcher.yf.download")
def test_fetch_ohlcv_empty_data(mock_download):
    # Arrange: empty DataFrame (invalid ticker or no data)
    mock_download.return_value = pd.DataFrame()

    # Act
    rows = fetch_ohlcv("INVALID", "1d")

    # Assert
    assert rows == []
