from fastapi import FastAPI
import os
import asyncpg
import redis.asyncio as aioredis

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Instrumentator for Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Database and Redis URLs
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/app")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!!"}

# Optional: async init for PostgreSQL and Redis (not yet connected to endpoints)
async def connect_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.close()

async def connect_redis():
    r = aioredis.from_url(REDIS_URL)
    await r.ping()
