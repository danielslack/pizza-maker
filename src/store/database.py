from typing import Optional
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from . import get_all_documents

from beanie import init_beanie


def db_instance():
    client = AsyncIOMotorClient("mongodb://localhost:27017/pizza_maker")
    list_of_documents = get_all_documents()
    return init_beanie(database=client.pizza_maker, document_models=list_of_documents)
