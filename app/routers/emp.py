from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
    UploadFile,
    File
)
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.emp import Employee

router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def employee_list(
        request: Request,
        db:AsyncSession = Depends(get_session)
):
    result = await db.execute(select(Employee).order_by(Employee.id))
    employees = result.scalars().all()

    return templates.TemplateResponse(
        "employees/list.html",
        {
            "request": request,
            "employees": employees
        }
    )

