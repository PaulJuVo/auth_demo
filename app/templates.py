from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/guests", response_class=HTMLResponse)
def read_guests(request: Request):
    users_list = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
    ]
    return templates.TemplateResponse(
        "guestlist.html", {"request": request, "users":users_list}
    )