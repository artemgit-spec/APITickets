from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated

from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session


from schemas.schemas_user import CreateUser
from db_management.db import session_db, User
from enums_status.status import NewStatusUser
from core.security import oaut2, get_hash_pass, decode_token


apirouter_user = APIRouter(prefix='/users', tags=["Работа с пользователями"])


#регистрация пользоватя
@apirouter_user.post('/reg-user')
async def create_user(
    db:Annotated[Session, Depends(session_db)],
    cr_us: CreateUser
):
    db.execute(insert(User).values(name = cr_us.name,
                                   password = get_hash_pass(cr_us.password),
                                   mail_users = cr_us.mail_user,
                                   is_admin = cr_us.is_admin))
    db.commit()
    return {'status_code':status.HTTP_201_CREATED,
            'detail':'Пользователь создан'}

#вывод всех пользователей
@apirouter_user.get('/all-users')
async def output_all_user(
    db:Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)]
):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный токен или срок действия токена истек')
    
    admin = payload.get('is_admin')
    if admin == 'admin':
        users = db.scalars(select(User)).all()
        return users
    else:
        return {'message':"недостаточно прав"}

#вывод информации по одному пользователю
@apirouter_user.get("/info-user/{id}")
async def info(
    id: int,
    db:Annotated[Session, Depends(session_db)] 
):
    user = db.scalar(select(User).where(User.id==id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет такого тикета'
        )
    return user



#обновление статуса по одному пользователю
@apirouter_user.patch("/update-status-user/{id}")
async def update_status(
    id: int,
    db: Annotated[Session, Depends(session_db)],
    new_status: NewStatusUser
):
    user = db.scalar(select(User).where(User.id==id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет такого тикета'
        )
    db.execute(update(User).where(User.id==id).values(
        is_admin = new_status
    ))
    db.commit()
    return {'status_code':status.HTTP_200_OK,
            'detail':'Статус изменен'}
    
