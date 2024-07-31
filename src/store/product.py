from typing import Optional
from beanie import Document, Indexed
from src.store.category import Category


class Product(Document):
    name: str
    description: Optional[str] = None
    price: Indexed(float)
    category: Category
