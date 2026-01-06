# Stock Market Data Service

A Python-based backend service that fetches stock market OHLCV (Open, High, Low, Close, Volume) data from Yahoo Finance, stores it locally using SQLite, and exposes the data through a REST API built with FastAPI.

This project is built to demonstrate clean architecture, separation of concerns, correct API usage, local persistence, and reliable automated testing.



## Objective

Build a small Python service that:

- Fetches stock market OHLCV data
- Stores the data locally with deduplication
- Exposes the data through a web server
- Is configurable, testable, and maintainable



## Features

- Fetches OHLCV data using Yahoo Finance (`yfinance`)
- Local storage using SQLite
- Deduplication handled at the database level
- REST API built with FastAPI
- Auto-generated API documentation using Swagger UI
- Unit tests with mocked external API calls
- Configurable behavior using environment variables



## Architecture Overview

Client (Browser / curl)
|
v
FastAPI (API Layer)
|
v
Fetcher (Yahoo Finance) <-- mocked in tests
|
v
SQLite Storage (Local DB)

## Project Outputs

### Tests & Server Execution
## Project Outputs

### Tests & Server Execution
![Tests and Server Execution](Outputs/OUTPUT%202.jpeg)

### Swagger UI & API Endpoints
![Swagger UI](Outputs/OUTPUT%201.jpeg)


### Separation of Concerns

- `fetcher.py` → Fetching and validating market data
- `storage.py` → Database logic and deduplication
- `api.py` → HTTP endpoints only
- `main.py` → Application entry point
- `models.py` → Data models / contracts
- `tests/` → Isolated, deterministic unit tests


## Project Structure

stock_service/
├── app/
│ ├── api.py
│ ├── fetcher.py
│ ├── main.py
│ ├── models.py
│ └── storage.py
├── tests/
│ ├── conftest.py
│ ├── test_api.py
│ ├── test_fetcher.py
│ └── test_storage.py
├── data/
│ ├── market.db
│ └── test.db
├── Outputs/
│ ├── output_1.jpeg
│ └── output_2.jpeg
├── requirements.txt
├── README.md
└── .gitignore



## Setup & Run Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd stock_service

2. Create and activate a virtual environment
python -m venv .venv

Windows
.venv\Scripts\activate


macOS / Linux
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Run tests (recommended)
pytest

All tests should pass before running the server.

5. Start the server
uvicorn app.main:app --reload

The service will be available at:

http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs


API Endpoints
POST /fetch?ticker=AAPL
Fetches OHLCV data for the given ticker and stores it locally.

GET /last
Returns the most recent stored data point.

GET /history
Returns all stored data points in chronological order.

All responses are returned in JSON format.



Project Outputs

Tests & Server Execution
The image below shows:
Virtual environment activation
All unit tests passing
FastAPI server running successfully


Swagger UI & API Endpoints
The image below shows:
Auto-generated Swagger UI
Available API endpoints
API ready for interaction


Testing Strategy
Tests written using pytest
External API calls fully mocked
No internet access required for tests
SQLite tested using temporary databases
FastAPI endpoints tested using TestClient



Run all tests using:
pytest



Design Decisions & Trade-offs
SQLite was chosen for simplicity and ease of local setup.
In production, this would likely be replaced with PostgreSQL.
On-demand fetching was chosen instead of scheduled jobs to keep the system deterministic and easy to test.
Deduplication is enforced using a composite primary key (ticker, timestamp) at the database level.


Assumptions & Limitations
Yahoo Finance data may be delayed and is not guaranteed to be real-time.
No authentication or rate limiting is implemented.
Corporate actions (splits, dividends) are not handled.
This service is intended for demonstration purposes, not live trading.



Extension Questions
How would this scale to handle multiple tickers concurrently?
Use asynchronous fetching or background workers with batch inserts.

How would you avoid API rate limits?
Introduce caching, request throttling, and scheduled fetch jobs.

What’s the first architectural change for production?
Replace SQLite with PostgreSQL and introduce a caching layer such as Redis.

What’s a trading-related pitfall of this setup?
Yahoo Finance data is not real-time and may not accurately reflect corporate actions, making it unsuitable for live trading decisions.




Final Notes
This project prioritizes clarity, correctness, and maintainability.
Each component is intentionally small, testable, and easy to reason about.
The goal was to build a service that a reviewer can confidently run, understand, and extend.

