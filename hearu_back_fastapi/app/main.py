from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
import os
from app.services import analysis


app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "hearU backend is running!"}

@app.post("/analyze")
async def analyze(email: str = Form(...), file: UploadFile = File(...)):
    result = await analysis.analyze_audio(file, email)
    return result