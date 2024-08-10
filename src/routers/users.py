from fastapi import APIRouter, HTTPException
from src.store.user import User
from src.auth.auth import hash_password
from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import BeforeValidator
from datetime import datetime
from bson import ObjectId
from typing import Annotated

router = APIRouter()


def get_id(v: ObjectId):
    print("Chamou a função.......")
    return str(v)


_object_id = Annotated[str, BeforeValidator(get_id)]


class GetUser(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: _object_id
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    create_at: datetime


@router.get("/get-user/{user_name}", response_model=GetUser)
async def get_user_by_username(user_name: str):
    return await User.get_by_username(username=user_name)


@router.get("/get-user-email/{email}", response_model=GetUser)
async def get_user_by_email(email: str):
    try:
        usuario = await User.get_by_email(email=email)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return usuario

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro: {str(error)}")


@router.post("/create-user")
async def create_user(user: User):
    user.hashed_password = hash_password(user.hashed_password)
    return await user.insert()
