from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from src.store.database import db_instance


@asynccontextmanager
async def lifespan(application: FastAPI):
    await db_instance()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    return {"message": "Hello Pizza Maker"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
