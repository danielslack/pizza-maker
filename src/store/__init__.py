import sys
from typing import Sequence, Type, TypeVar
from inspect import isclass, getmembers
from beanie import Document
from .product import Product
from .user import User
from .category import Category

DocType = TypeVar("DocType", bound=Document)


def get_all_documents() -> Sequence[Type[DocType]]:
    return [
        doc
        for _, doc in getmembers(sys.modules[__name__], isclass)
        if issubclass(doc, Document) and doc.__name__ != "Document"
    ]
