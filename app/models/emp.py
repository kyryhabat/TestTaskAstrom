from datetime import date

from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    last_name: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    birth_date: Mapped[date] = mapped_column(Date)

    phone: Mapped[str | None] = mapped_column(String(20))

    gender: Mapped[str] = mapped_column(String(10))

    photo_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

