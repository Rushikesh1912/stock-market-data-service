from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.api import storage

client = TestClient(app)


def clear_db():
    storage.conn.execute("DELETE FROM market_data")
    storage.conn.commit()


@patch("app.api.fetch_ohlcv")
def test_fetch_endpoint(mock_fetch):
    clear_db()

    mock_fetch.return_value = [
        ("AAPL", "2024-01-01T00:00:00", 100, 110, 90, 105, 1000)
    ]

    response = client.post("/fetch?ticker=AAPL")

    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert data["fetched"] == 1
    assert data["inserted"] == 1


def test_get_last_empty_db():
    clear_db()

    response = client.get("/last")
    assert response.status_code == 404


@patch("app.api.fetch_ohlcv")
def test_history_endpoint(mock_fetch):
    clear_db()

    mock_fetch.return_value = [
        ("AAPL", "2024-01-01T00:00:00", 100, 110, 90, 105, 1000)
    ]

    client.post("/fetch?ticker=AAPL")

    response = client.get("/history")

    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) == 1
