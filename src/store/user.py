from beanie import Document, Indexed
from datetime import datetime
from pydantic import EmailStr
from pydantic.fields import Field
from typing import Optional, Union, Any


class User(Document):
    username: Indexed(str, unique=True)  # type: ignore[valid-type]
    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    create_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def get_by_username(cls, *, username: str) -> Optional["User"]:
        return await cls.find_one(cls.username == username.lower())

    @classmethod
    async def get_by_api_key(cls, *, api_key: str) -> Optional["User"]:
        return await cls.find_one(cls.api_key == api_key.lower())

    @classmethod
    async def authenticate(cls, *, username: str, password: str) -> Any:
        user = await cls.get_by_username(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None

        return User

    class Settings:
        name = "users"
        use_state_management = True
