import pytest

import asyncio

from beanie.odm.operators.update.general import Set

from src.store.database import db_instance
from src.store.product import Product
from src.store.category import Category


pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
async def test_create_or_update_product():
    db = await db_instance()
    category = Category(name="Pizza", description="Todas as pizzas")
    product = Product(
        name="Marguerita",
        description="Pizza sabor Marguerita",
        price=12.0,
        category=category,
    )
    item = await Product.find_one(Product.name == product.name).upsert(
        Set({Product.name: product.name}), on_insert=product
    )
