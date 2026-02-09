from fastapi import Request
from app.main import templates

async def chat_loading(request: Request):
    return templates.TemplateResponse(
        "chat_loading.html",
        {"request": request}
    )