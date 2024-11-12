import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import date
from app import db
from enum import Enum


class CurrencyEnum(Enum):
    PEN = "soles"
    USD = "dólares"
    NONE = "no identificado"

class Email(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)

class Transaction(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('email.id'), nullable=False)
    transaction_date: so.Mapped[date] = so.mapped_column(sa.Date, default=date.today)
    transaction_code: so.Mapped[str] = so.mapped_column(sa.String(255))
    issuer: so.Mapped[str] = so.mapped_column(sa.String(255))
    source: so.Mapped[str] = so.mapped_column(sa.String(255))
    destination: so.Mapped[str] = so.mapped_column(sa.String(255))
    currency: so.Mapped[CurrencyEnum] = so.mapped_column(sa.Enum(CurrencyEnum), nullable=False)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
