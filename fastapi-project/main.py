from fastapi import FastAPI

from app.todos import router

app = FastAPI()

app.include_router(router)


