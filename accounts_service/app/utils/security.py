import os
from dotenv import load_dotenv
from jwt import PyJWTError
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY.strip(), algorithms=["HS256"])
        return payload
    except PyJWTError:
        return None
