from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC

from db_management.db import session_db, User
from core.config import settings

"""
данные для входа
{
  "name": "admin",
  "password": "admin",
  "mail_user": "user@example.com",
  "is_admin": "admin"
}
{
  "name": "user",
  "password": "user",
  "mail_user": "user@example.com",
  "is_admin": "user"
}
"""

apirouter_auth = APIRouter(tags=["Работа с пользователями"])

oaut2 = OAuth2PasswordBearer(tokenUrl="token")
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# функция для хэширования пароля
def get_hash_pass(password):
    return bcrypt.hash(password)


# функция для проверки пароля
def verify_pass(plain_pass, hash_pass):
    return bcrypt.verify(plain_pass, hash_pass)


# функция для создания токена
def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# функция для проверки токена
def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


# авторизация пользователя и создание токена
@apirouter_auth.post("/token")
async def login(
    date_auth: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(session_db)],
):
    username = date_auth.username
    password = date_auth.password
    user = db.scalar(select(User).where(User.name == username))
    if not user or not verify_pass(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль"
        )
    token_data = {
        "id": user.id,
        "name": user.name,
        "password": user.password,
        "is_admin": user.is_admin,
    }
    access_token = create_token(data=token_data, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
