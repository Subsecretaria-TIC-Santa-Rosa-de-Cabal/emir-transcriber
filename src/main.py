from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import whisper
import tempfile
import os
from pathlib import Path
from enum import Enum

class Calidad(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transcribir/")
async def transcribir_audio(archivo: UploadFile = File(...), calidad: Calidad = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await archivo.read())
        tmp_path = tmp.name

    if calidad == Calidad.ALTA:
        model_name = "large"
    elif calidad == Calidad.MEDIA:
        model_name = "medium"
    else:
        model_name = "small"

    model = whisper.load_model(model_name)
    result = model.transcribe(tmp_path)

    segmentos = []
    for seg in result["segments"]:
        segmentos.append(f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}")

    texto = "\n".join(segmentos)

    base_name, _ = os.path.splitext(archivo.filename)
    txt_filename = f"{base_name}.txt"
    txt_path = tmp_path.replace(".mp3", ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(texto)

    os.remove(tmp_path)
    return FileResponse(txt_path, media_type="text/plain", filename=txt_filename)
