from fastapi import FastAPI, Request
from . import models
from .database import engine
from .routers import todos, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allowed frontend origins
origins = [
    "http://127.0.0.1:5500",  
    "http://localhost:5500",  
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# CORS Middleware allows frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static files (for CSS, JS, images)
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

# Load Jinja2 templates
templates = Jinja2Templates(directory="TodoApp/templates")

app.include_router(todos.router)
app.include_router(auth.router)

# Everything handled in index.html
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
