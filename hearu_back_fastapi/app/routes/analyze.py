# app/routes/analyze.py
from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from app.services.analysis import analyze_audio

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile, email: str = Form(...)):
    try:
        result = await analyze_audio(file, email)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

