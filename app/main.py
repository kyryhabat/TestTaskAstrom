from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import engine
from app.models.emp import Base
from app.routers.emp import router as emp_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(emp_router)

app.mount("/static",
          StaticFiles(directory="app/static"),
          name="static"
          )
