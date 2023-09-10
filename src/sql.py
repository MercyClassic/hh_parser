from sqlalchemy import insert, select

from db.database import session_maker
from models import CheckedVacancy


def is_checked(link: str) -> bool:
    query = select(1).where(CheckedVacancy.url.is_(link))
    with session_maker() as session:
        result = session.execute(query)

    return result.scalar()


def set_check(link: str) -> None:
    stmt = insert(CheckedVacancy).values(url=link)
    with session_maker() as session:
        session.execute(stmt)
        session.commit()
