from fastapi import FastAPI
import logging
from .dependencies import database

logger = logging.getLogger("uvicorn")

app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("--- Start initialising DB ---")
    database.init_db()
    logger.info("--- Finished DB init ---")

@app.get("/")
def read_root():
    return {"Hello": "World 4"}