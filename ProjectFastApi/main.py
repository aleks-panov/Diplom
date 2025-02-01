from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

app = FastAPI()

# Настройка папки для загруженных файлов
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Монтирование статической папки
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload/")
async def upload_photo(title: str = Form(...), image: UploadFile = File(...)):
    # Сохраняем файл
    file_path = Path(UPLOAD_FOLDER) / image.filename
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())
    return {"message": f"Photo '{title}' uploaded successfully!"}


@app.get("/", response_class=HTMLResponse)
async def photo_list():
    photos = os.listdir(UPLOAD_FOLDER)
    content = """
    <h1>Фотографии</h1>
    <a href="/upload">Загрузить фото</a>
    <ul>
    """
    for photo in photos:
        content += f"""
        <li>
            <img src="/static/uploads/{photo}" alt="{photo}" width="200">
            <p>{photo}</p>
            <form action="/delete/{photo}" method="post">
                <button type="submit">Удалить</button>
            </form>
        </li>
        """
    content += "</ul>"
    return content


@app.post("/delete/{filename}")
async def delete_photo(filename: str):
    file_path = Path(UPLOAD_FOLDER) / filename
    if file_path.exists():
        file_path.unlink()  # Удаляем файл
        return {"message": f"Photo '{filename}' deleted successfully!"}
    raise HTTPException(status_code=404, detail=f"Photo '{filename}' not found!")


@app.get("/upload", response_class=HTMLResponse)
async def upload_form():
    return """
    <h1>Загрузить фото</h1>
    <form action="/upload/" method="post" enctype="multipart/form-data">
        <label for="title">Title:</label>
        <input type="text" name="title" required><br><br>
        <label for="image">Image:</label>
        <input type="file" name="image" required><br><br>
        <button type="submit">Загрузить</button>
    </form>
    <a href="/">Назад</a>
    """