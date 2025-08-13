from pydantic import BaseModel
from datetime import datetime


class CreateTickets(BaseModel):
    title: str
    text_ticket: str
    creating_ticket: datetime


class UpdateTicket(BaseModel):
    title: str
    text_ticket: str


class UpdateStatusTicket(BaseModel):
    closing_ticket: datetime


class TicketModel(BaseModel):
    title: str
    text_ticket: str
    creating_ticket: datetime
    is_active: bool


class InfoTicket(BaseModel):
    title: str
    text_ticket: str
    is_active: str
