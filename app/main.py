from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Stock Market Data Service")

app.include_router(router)
