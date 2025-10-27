# Assumes the FastAPI app from above is already defined
import secrets
import uuid
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Response
import os
from dotenv import load_dotenv
# Load .env file
load_dotenv("./.env")


app = FastAPI()
secret_key = secrets.token_urlsafe(32)
app.add_middleware(
    SessionMiddleware, secret_key=secret_key
)  

@app.get("/", response_class=HTMLResponse)
async def chatbot_page(request: Request, response: Response):
    client_id = request.session.get("client_id")
    if client_id is None:
        client_id = str(uuid.uuid4())  # Generate a new UUID
        request.session["client_id"] = client_id
        response.set_cookie(key="client_id", value=client_id)
    templates = Jinja2Templates(directory=".")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_host": "127.0.0.1"
        },
    )

@app.post("/chat/", status_code=201)
async def chat(data: dict, request: Request):
    
    client_id = request.session.get("client_id")
    print(f"input={data}")
    output = "hello to chat"
    return {"text": f"input={data}"}