from fastapi import FastAPI
from . import models
from .database import engine
from .routers import todos,auth


models.Base.metadata.create_all(bind=engine)

app=FastAPI()


app.include_router(todos.router)
app.include_router(auth.router)

@app.get("/")
def root() :
    return {"data" : "It is running properly"}