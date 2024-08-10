import jwt
from pydantic import BaseModel
import datetime
import pytz  # type: ignore[missing-imports]
import time
from typing import Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ALG = "HS256"
SECRET = "MY_TOKEN_SECRET"


class TokenData(BaseModel):
    name: str
    email: str


class TokenDataDecode(TokenData):
    exp: int


def hash_password(password: str) -> str:
    password_hasher = PasswordHasher()
    return password_hasher.hash(password)


def verify_password(hash_password: str, password: str):
    try:
        password_hasher = PasswordHasher()
        return password_hasher.verify(hash_password, password)
    except VerifyMismatchError as error:
        return False
    except Exception as error:
        print(error)


def encode_token(paylod_token: TokenData, seconds: int) -> str:
    exp = datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(seconds=seconds)
    paylod = dict(paylod_token)
    paylod.update({"exp": exp})
    token_str = jwt.encode(paylod, SECRET, algorithm=ALG)
    return token_str


def decode_token(token: str) -> dict[str, str]:
    try:
        token_data: TokenDataDecode = jwt.decode(token, SECRET, algorithms=[ALG])
        return dict(token_data)
    except jwt.ExpiredSignatureError as expires_error:
        return dict(message="error", error=str(expires_error))
    except jwt.InvalidSignatureError as signature_error:
        return dict(message="error", error=str(signature_error))
    except Exception as error:
        return {"error": str(error)}
