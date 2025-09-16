import logging
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.routers import example
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Name of your API", lifespan=lifespan)

# Add your Routers here:
app.include_router(example.router)
