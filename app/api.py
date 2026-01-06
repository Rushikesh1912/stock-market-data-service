import os
from fastapi import APIRouter, HTTPException
from app.fetcher import fetch_ohlcv
from app.storage import SQLiteStorage
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

DB_PATH = os.getenv("DB_PATH", "./data/market.db")
DEFAULT_INTERVAL = os.getenv("DEFAULT_INTERVAL", "1d")

storage = SQLiteStorage(DB_PATH)


@router.post("/fetch")
def fetch_and_store(ticker: str):
    rows = fetch_ohlcv(ticker, DEFAULT_INTERVAL)

    if not rows:
        raise HTTPException(
            status_code=400,
            detail="No data returned. Invalid ticker or empty result.",
        )

    inserted = storage.insert_many(rows)
    return {
        "ticker": ticker.upper(),
        "fetched": len(rows),
        "inserted": inserted,
    }


@router.get("/last")
def get_last():
    row = storage.fetch_latest()

    if not row:
        raise HTTPException(status_code=404, detail="No data found")

    return {
        "ticker": row[0],
        "timestamp": row[1],
        "open": row[2],
        "high": row[3],
        "low": row[4],
        "close": row[5],
        "volume": row[6],
    }


@router.get("/history")
def get_history():
    rows = storage.fetch_all()

    return [
        {
            "ticker": r[0],
            "timestamp": r[1],
            "open": r[2],
            "high": r[3],
            "low": r[4],
            "close": r[5],
            "volume": r[6],
        }
        for r in rows
    ]
