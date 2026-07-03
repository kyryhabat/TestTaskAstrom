
from datetime import date

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
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.database import get_session
from app.models.emp import Employee
from app.utils.files import save_photo

PAGE_SIZE = 10
router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/create")
async def create_employee_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="employees/form.html",
        context={"employee": None},
    )

@router.get("/")
async def employee_list(
    request: Request,
    db: AsyncSession = Depends(get_session),
    page: int = 1,
    q: str | None = None,
    gender: str | None = None,
    age_from: str | None = None,
    age_to: str | None = None,
):

    age_from_int = int(age_from) if age_from else None
    age_to_int = int(age_to) if age_to else None

    query = select(Employee)


    if q:
        query = query.where(
            or_(
                Employee.first_name.ilike(f"%{q}%"),
                Employee.last_name.ilike(f"%{q}%"),
                Employee.phone.ilike(f"%{q}%"),
            )
        )


    if gender:
        query = query.where(Employee.gender == gender)


    result = await db.execute(
        query.order_by(Employee.id)
    )

    employees = result.scalars().all()


    if age_from_int is not None:
        employees = [
            employee
            for employee in employees
            if employee.age >= age_from_int
        ]

    if age_to_int is not None:
        employees = [
            employee
            for employee in employees
            if employee.age <= age_to_int
        ]


    total = len(employees)

    total_pages = max(
        1,
        (total + PAGE_SIZE - 1) // PAGE_SIZE
    )

    if page < 1:
        page = 1

    if page > total_pages:
        page = total_pages

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    employees = employees[start:end]

    return templates.TemplateResponse(
        request=request,
        name="employees/list.html",
        context={
            "employees": employees,
            "page": page,
            "total_pages": total_pages,
            "query": q,
            "gender_filter": gender,
            "age_from": age_from,
            "age_to": age_to,
        },
    )
@router.post("/create")
async def create_employee(
        first_name: str = Form(...),
        last_name: str = Form(...),
        middle_name: str | None = Form(None),
        birth_date: date = Form(...),
        phone: str | None = Form(None),
        gender: str = Form(...),
        photo: UploadFile | None = File(None),
        db:AsyncSession = Depends(get_session)
):
    filename = None
    if photo and photo.filename:
        filename = await save_photo(photo)



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

@router.get("/{employee_id}/update")
async def edit_employee_page(
        request: Request,
        employee_id: int,
        db: AsyncSession = Depends(get_session),
):
    employee = await db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    return templates.TemplateResponse(
        request=request,
        name="employees/form.html",
        context={"employee": employee},
    )

@router.post("/{employee_id}/update")
async def update_employee(
        employee_id: int,
        db:AsyncSession = Depends(get_session),
        first_name: str = Form(...),
        last_name: str = Form(...),
        middle_name: str | None = Form(None),
        birth_date: date = Form(...),
        phone: str | None = Form(None),
        gender: str = Form(...),
        photo: UploadFile | None = File(None),
):
    employee = await db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    employee.first_name = first_name
    employee.last_name = last_name
    employee.middle_name = middle_name
    employee.birth_date = birth_date
    employee.phone = phone
    employee.gender = gender


    if photo and photo.filename:
        employee.photo_path = await save_photo(photo)

    await db.commit()
    await db.refresh(employee)

    return RedirectResponse(
        url="/employee/",
        status_code=303
    )

@router.post("/{employee_id}/delete")
async def delete_employee(
        employee_id: int,
        db: AsyncSession = Depends(get_session),
):
    employee = await db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    await db.delete(employee)
    await db.commit()

    return RedirectResponse(url="/employee/", status_code=303)




