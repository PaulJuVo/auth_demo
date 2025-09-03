from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import logging

from .authentication import auth_controller as auth
from .core import database
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import templates as templates_router


logger = logging.getLogger("uvicorn")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(templates_router.router, prefix="/templates",
    tags=["templates"],)
app.include_router(auth.router,tags=["Authentication"])

@app.on_event("startup")
def on_startup():
    logger.info("--- Start initialising DB ---")
    database.init_db()
    logger.info("--- Finished DB init ---")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return FileResponse("frontend/index.html")


