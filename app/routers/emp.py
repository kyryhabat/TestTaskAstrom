import uuid
from datetime import date
from pathlib import Path
from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
    UploadFile,
    File, HTTPException
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.database import get_session
from app.models.emp import Employee

UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def employee_list(
        request: Request,
        db:AsyncSession = Depends(get_session),
        title = "Получение всех сотрудников"
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

@router.post("/create")
async def create_employee(
        first_name: str = Form(...),
        last_name: str = Form(...),
        middle_name: str | None = Form(None),
        birth_date: date = Form(...),
        phone: str | None = Form(...),
        gender: str = Form(...),
        photo: UploadFile | None = File(None),
        db:AsyncSession = Depends(get_session)
):
    filename = None

    if photo and photo.filename:
        content = await photo.read()

        if len(content) > 200 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Фото должно быть менее 200 КБ"
            )

        extension = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"

        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(content)


    new_employee = Employee(
    last_name = last_name,
    first_name = first_name,
    middle_name = middle_name,
    birth_date = birth_date,
    phone = phone,
    gender = gender,
    photo_path = filename,
    )

    db.add(new_employee)
    await db.commit()
    await db.refresh(new_employee)

    return RedirectResponse(
        url="/employee/",
        status_code=303
    )
