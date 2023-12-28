from fastapi import FastAPI
from app.router import router
from app.database import Base, engine

app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
