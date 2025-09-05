from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import logging

from .auth import auth_controller as auth
from .user import user_controller
from .core import database
from fastapi.staticfiles import StaticFiles
from . import templates as templates_router


logger = logging.getLogger("uvicorn")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(templates_router.router, prefix="/templates",
    tags=["templates"],)
app.include_router(auth.router,tags=["Authentication"])
app.include_router(user_controller.router, prefix="/users", tags=["users"])




@app.on_event("startup")
def on_startup():
    logger.info("--- Start initialising DB ---")
    database.init_db()
    logger.info("--- Finished DB init ---")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return FileResponse("frontend/index.html")


