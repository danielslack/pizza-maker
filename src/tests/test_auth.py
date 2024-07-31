import pytest
from src.auth.auth import encode_token, decode_token
import datetime
import pytz
import time
import jwt

PAYLOAD = {"name": "Daniel Caria", "email": "daniel.slack2@gmail.com"}

EXP = datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(seconds=5)


@pytest.fixture
def jwt_token():
    token_str = encode_token(PAYLOAD, 5)
    return token_str


def modify_jwt_token(jwt_token):
    token_data = decode_token(jwt_token)
    token_data["name"] = "Daniel A Caria"
    fake_token = jwt.encode(token_data, "FAKE_SECRET", "HS256")
    return fake_token


def test_encode_token():
    token_str = encode_token(PAYLOAD, 5)
    assert isinstance(token_str, str)


def test_decode_token(jwt_token):
    token_data = decode_token(jwt_token)
    token_keys = token_data.keys()
    assert isinstance(token_data, dict)
    assert list(token_keys) == ["name", "email", "exp"]
    assert token_data["name"] == "Daniel Caria"
    assert token_data["email"] == "daniel.slack2@gmail.com"
    assert token_data["exp"] == int(datetime.datetime.timestamp(EXP))


def test_token_expires(jwt_token):
    time.sleep(7)
    token_data = decode_token(jwt_token)
    assert token_data == {"message": "error", "error": "Signature has expired"}


def test_token_spoofing(jwt_token):
    token_spoofing = modify_jwt_token(jwt_token)
    token_data = decode_token(token_spoofing)
    assert token_data == {"message": "error", "error": "Signature verification failed"}
