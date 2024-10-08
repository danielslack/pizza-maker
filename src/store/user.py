from beanie import Document, Indexed
from datetime import datetime
from pydantic import EmailStr
from pydantic.fields import Field
from typing import Optional, Union, Any
from src.auth.auth import verify_password, encode_token, TokenData


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
    async def get_by_email(cls, *, email: str) -> Optional["User"]:
        return await cls.find_one(cls.email == email.lower())

    @classmethod
    async def authenticate(cls, *, username: str, password: str):
        if "@" in username:
            user = await cls.get_by_email(email=username)
        else:
            user = await cls.get_by_username(username=username)

        if not user or not user.is_active or not verify_password(user.hashed_password, password):
            return None

        token = TokenData(username=user.username, email=user.email)

        return encode_token(token, seconds=60 * 60 * 24)

    class Settings:
        name = "users"
        use_state_management = True
