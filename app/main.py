from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.emp import router as emp_router

app = FastAPI()

app.include_router(emp_router)

app.mount("/static",
          StaticFiles(directory="app/static"),
          name="static"
          )
