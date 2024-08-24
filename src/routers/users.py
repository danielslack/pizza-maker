from fastapi import APIRouter, HTTPException
from src.store.user import User
from src.auth.auth import hash_password
from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import BeforeValidator
from datetime import datetime
from bson import ObjectId
from typing import Annotated, Optional
from beanie import Document

router = APIRouter()


def get_id(v: ObjectId):
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


class UpdateUser(BaseModel):
    id: _object_id
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class LoginUser(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    token: str


@router.get("/get-user/{user_name}", response_model=GetUser)
async def get_user_by_username(user_name: str):
    """
    Retorna os dados do usuário, a busca é realizada utilizando o nome do usuário:
    """
    try:
        if user := await User.get_by_username(username=user_name):
            return user
        else:
            raise HTTPException(status_code=204, detail="Usuário não encontrado")

    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro: {str(error)}")


@router.get("/get-user-email/{email}", response_model=GetUser)
async def get_user_by_email(email: str):
    """
    Retorna os dados do usuário, a busca é realizado utlizando o e-mail do usuário
    """
    try:
        usuario = await User.get_by_email(email=email)
        if not usuario:
            raise HTTPException(status_code=204, detail="Usuário não encontrado")

        return usuario

    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro: {str(error)}")


@router.post("/create-user", status_code=201)
async def create_user(user: User):
    """
    Cria um novo usuário no sistema
    """
    try:
        user.hashed_password = hash_password(user.hashed_password)
        return await user.insert()
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro: {str(error)}")


@router.put("/update-user")
async def update_user(user_data: UpdateUser):
    """
    Atualiza o usuário no sistema
    """
    try:
        user = await User.get(user_data.id)
        if not user:
            raise HTTPException(status_code=204, detail="Usuário não encontrado")

        if user_data.password:
            user.hashed_password = hash_password(user_data.password)

        user.email = user_data.email if user_data.email else user.email
        user.username = user_data.username if user_data.username else user.username

        await user.save()

    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro: {str(error)}")


@router.post("/login", response_model=TokenData)
async def login_user(user_login: LoginUser):
    """
    Faz o login no sistema, pode ser utilizado o nome do usuário ou seu e-mail
    """
    try:
        token_str = await User.authenticate(username=user_login.username, password=user_login.password)
        if not token_str:
            raise HTTPException(status_code=204, detail="Usuário não encontrado ou senha está errada")

        return TokenData(token=token_str)

    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro: {str(error)}")


@router.patch("/disable-user/{user_id}")
async def disable_user(user_id: str):
    """
    Desabilita o usuário, seus dados ainda estará armazenado no sistema.
    Caso deseje remover o usuário utilizar o endpoint /remover-user
    """
    try:
        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=204, detail="Usuário não encontrado")

        user.is_active = False
        await user.save()

    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro {str(error)}")


@router.delete("/remove-user/{user_id}", status_code=204)
async def remove_user(user_id: str):
    """
    Remove o usuário e todos os seus registros da base de dados.
    Caso deseje manter o registro, utilize o endpoint /disable_user.
    """
    try:
        user = await User.get(user_id)
        if user:
            await user.delete()

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro: {str(error)}")
