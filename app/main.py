# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import telegram
from app.middleware.logging import LoggingMiddleware
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title=settings.app_name)

app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(LoggingMiddleware)

app.include_router(telegram.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "ISP-Sentinel AI Running", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)