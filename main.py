import uvicorn 
import python_multipart

from fastapi import FastAPI
from routers.rout_tickets import apirouter_tickets
from routers.rout_user import apirouter_user
from core.security import apirouter_auth

app = FastAPI(title='Tickets')

app.include_router(apirouter_tickets)
app.include_router(apirouter_user)
app.include_router(apirouter_auth)


if __name__=="__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True)
    
"""
Добавить:
1)Работу с пользователя: регистрация, аутентификация, авторизация, смена прав
2)Добавить логгирование
3)Добавить отправку писем при смене статуса тикета    
"""