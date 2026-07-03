from datetime import date

from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    birth_date: date
    phone: str | None = None
    gender: str

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None
    birth_date: date
    phone: str
    gender: str

    model_config = ConfigDict(
        from_attributes=True
    )
