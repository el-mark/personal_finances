import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Email(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    from_email: so.Mapped[str] = so.mapped_column(sa.String(255))
