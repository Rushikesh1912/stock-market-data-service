import sqlite3
from pathlib import Path
from typing import Iterable, Tuple


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS market_data (
    ticker TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER NOT NULL,
    PRIMARY KEY (ticker, timestamp)
);
"""


class SQLiteStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._initialize()

    def _initialize(self) -> None:
        self.conn.execute(SCHEMA_SQL)
        self.conn.commit()

    def insert_many(self, rows: Iterable[Tuple]) -> int:
        query = """
        INSERT OR IGNORE INTO market_data
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.conn.executemany(query, rows)
        self.conn.commit()
        return cursor.rowcount

    def fetch_latest(self):
        cursor = self.conn.execute(
            "SELECT * FROM market_data ORDER BY timestamp DESC LIMIT 1"
        )
        return cursor.fetchone()

    def fetch_all(self):
        cursor = self.conn.execute(
            "SELECT * FROM market_data ORDER BY timestamp ASC"
        )
        return cursor.fetchall()
