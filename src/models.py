from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class CheckedVacancy(Base):
    __tablename__ = 'checked_vacancy'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
