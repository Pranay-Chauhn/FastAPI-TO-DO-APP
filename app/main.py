from fastapi import FastAPI
from . import models
from .database import engine
from .router import tasks, users, login
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"data": "Hello World"}

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(login.router)

