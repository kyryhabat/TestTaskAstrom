

from fastapi import UploadFile,HTTPException
from pathlib import Path
import uuid


UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def save_photo(photo: UploadFile) -> str:
    content = await photo.read()

    if len(content) > 200 * 1024:
        raise HTTPException(status_code=400, detail="Фото должно быть менее 200 КБ")

    extension = photo.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(content)

    return f"uploads/{filename}"   # ← храним путь ОТНОСИТЕЛЬНО /static