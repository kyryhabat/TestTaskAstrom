from datetime import date

from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    birth_date: date
    phone: str
    gender: str

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
