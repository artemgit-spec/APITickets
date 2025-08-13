from fastapi import APIRouter, Depends, status, HTTPException, Query, Form
from fastapi.responses import JSONResponse

from typing import Annotated
from datetime import datetime

from db_management.db import Ticket, session_db
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from schemas.schemas_tickets import (
    CreateTickets,
    TicketModel,
    UpdateTicket,
    UpdateStatusTicket,
    InfoTicket,
)
from enums_status.status import StatusTicket, NewStatus
from core.security import oaut2, get_hash_pass, decode_token


apirouter_tickets = APIRouter(prefix="/tickets", tags=["Работа с тикетами"])

# подумать о возможночти добавить комментарии к тикетам


# получаем список всех тикетов
@apirouter_tickets.get("/")
async def all_tickets(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)],
    status_ticket: StatusTicket = Query(),
):
    payload = decode_token(token)
    tickets = select(Ticket)

    if payload.get("is_admin") == "admin":

        if status_ticket == StatusTicket.all:
            stti = tickets
        elif status_ticket == StatusTicket.active:
            stti = tickets.where(Ticket.is_active == "active")
        elif status_ticket == StatusTicket.not_active:
            stti = tickets.where(Ticket.is_active == "not active")
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Такого фильтра нет"
            )
        result = db.scalars(stti).all()

    else:
        stti = tickets.where(Ticket.is_active == "active")
        result = db.scalars(stti).all()

    return result


# смотреть историю тикетов одного пользователя
@apirouter_tickets.get("/history-ticket/")
async def history_tickets_user(
    db: Annotated[Session, Depends(session_db)], token: Annotated[str, Depends(oaut2)]
):
    payload = decode_token(token)
    id = payload.get("id")
    tickets_users = db.scalar(select(Ticket).where(Ticket.id_user == id))
    return tickets_users


# создаем новый тикет
@apirouter_tickets.post("/create")
async def create_tickets(
    new_ticket: CreateTickets,
    token: Annotated[str, Depends(oaut2)],
    db: Annotated[Session, Depends(session_db)],
):
    payload = decode_token(token)

    db.execute(
        insert(Ticket).values(
            title=new_ticket.title,
            text_ticket=new_ticket.text_ticket,
            creating_ticket=new_ticket.creating_ticket.replace(tzinfo=None),
            id_user=payload.get("id"),
        )
    )

    db.commit()

    return JSONResponse(
        content={"detail": "Тикет создан"}, status_code=status.HTTP_201_CREATED
    )


# получаем информацию об одно тикете
@apirouter_tickets.get("/info-tickte/{id}", response_model=InfoTicket)
async def info_ticket(
    id: int,
    token: Annotated[str, Depends(oaut2)],
    db: Annotated[Session, Depends(session_db)],
):
    ticket = db.scalar(select(Ticket).where(Ticket.id == id))
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого тикета"
        )

    return ticket


# обновляем информацию о тикете
@apirouter_tickets.patch("/update-info/{id}")
async def update_tickets(
    id: int,
    up_tic: UpdateTicket,
    token: Annotated[str, Depends(oaut2)],
    db: Annotated[Session, Depends(session_db)],
):
    payload = decode_token(token)
    if payload.get("is_admin") == "admin":
        ticket = db.scalar(select(Ticket).where(Ticket.id == id))
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого тикета"
            )
        if up_tic.title == "string" and up_tic.text_ticket == "string":

            return {
                "status_code": status.HTTP_200_OK,
                "detail": "Информация не была обновлена",
            }

        elif up_tic.title != "string" and up_tic.text_ticket == "string":

            db.execute(
                update(Ticket)
                .where(Ticket.id == id)
                .values(
                    title=up_tic.title,
                    text_ticket=ticket.text_ticket,
                )
            )
            db.commit()
            return {
                "status_code": status.HTTP_200_OK,
                "detail": "Изменено название тикета",
            }

        elif up_tic.title == "string" and up_tic.text_ticket != "string":

            db.execute(
                update(Ticket)
                .where(Ticket.id == id)
                .values(
                    title=ticket.title,
                    text_ticket=up_tic.text_ticket,
                )
            )
            db.commit()
            return {
                "status_code": status.HTTP_200_OK,
                "detail": "Изменено содержание тикета",
            }
        else:
            db.execute(
                update(Ticket)
                .where(Ticket.id == id)
                .values(
                    title=up_tic.title,
                    text_ticket=up_tic.text_ticket,
                )
            )
            db.commit()
            return {
                "status_code": status.HTTP_200_OK,
                "detail": "Изменено название и текст тикета",
            }
    else:
        return {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "Не достаточно прав",
        }


# назначаем пользователя на тикет
@apirouter_tickets.patch("/update-user-ticket/{id}")
async def user_ticket(
    id: int,
    new_user: Annotated[int, Form()],
    token: Annotated[str, Depends(oaut2)],
    db: Annotated[Session, Depends(session_db)],
):
    payload = decode_token(token)
    ticket = db.scalar(select(Ticket).where(Ticket.id == id))
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого тикета"
        )
    if payload.get("is_admin") == "admin":
        db.execute(update(Ticket).where(Ticket.id == id).values(id_user=new_user))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Назначен новый пользователь на тикет",
    }


# обновляем статус тикета
@apirouter_tickets.patch("/update-status/{id}")
async def status_update(
    id: int,
    new_status: NewStatus,
    token: Annotated[str, Depends(oaut2)],
    db: Annotated[Session, Depends(session_db)],
):
    ticket = db.scalar(select(Ticket).where(Ticket.id == id))
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого тикета"
        )
    payload = decode_token(token)

    if payload.get("is_admin") == "admin":
        db.execute(
            update(Ticket)
            .where(Ticket.id == id)
            .values(is_active=new_status, closing_ticket=datetime.now())
        )
        db.commit()
        return {"status_code": status.HTTP_200_OK, "detail": "Тикет обновлен"}

    else:
        if new_status == NewStatus.active and ticket.is_active == NewStatus.not_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Закрытый тикет уже нельзя открыть",
            )
        else:
            db.execute(
                update(Ticket)
                .where(Ticket.id == id)
                .values(is_active=new_status, closing_ticket=datetime.now())
            )
            db.commit()
            return {"status_code": status.HTTP_200_OK, "detail": "Тикет обновлен"}


# удаляем один тикет
@apirouter_tickets.delete("/delete/{id}")
async def delete_ticket(
    id: int,
    token: Annotated[str, Depends(oaut2)],
    db: Annotated[Session, Depends(session_db)],
):
    ticket = db.scalar(select(Ticket).where(Ticket.id == id))
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого тикета"
        )
    payload = decode_token(token)
    if payload.get("is_admin") == "admin":

        db.execute(delete(Ticket).where(Ticket.id == id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "detail": "Тикет удален"}
    else:
        return {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "Не достаточно прав",
        }
