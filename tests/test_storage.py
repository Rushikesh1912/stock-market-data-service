import os
from app.storage import SQLiteStorage


def test_insert_and_deduplication(tmp_path):
    db_path = tmp_path / "test.db"
    storage = SQLiteStorage(str(db_path))

    rows = [
        ("AAPL", "2024-01-01T00:00:00", 100, 110, 90, 105, 1000),
        ("AAPL", "2024-01-01T00:00:00", 100, 110, 90, 105, 1000),  # duplicate
    ]

    inserted = storage.insert_many(rows)

    assert inserted == 1
    all_rows = storage.fetch_all()
    assert len(all_rows) == 1


def test_fetch_latest(tmp_path):
    db_path = tmp_path / "test.db"
    storage = SQLiteStorage(str(db_path))

    rows = [
        ("AAPL", "2024-01-01T00:00:00", 100, 110, 90, 105, 1000),
        ("AAPL", "2024-01-02T00:00:00", 106, 112, 95, 110, 1500),
    ]

    storage.insert_many(rows)

    latest = storage.fetch_latest()

    assert latest[1] == "2024-01-02T00:00:00"
    assert latest[6] == 1500
