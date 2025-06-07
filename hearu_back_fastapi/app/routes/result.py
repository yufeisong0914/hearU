# app/routes/result.py

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson.regex import Regex

router = APIRouter()

client = MongoClient("mongodb+srv://yufeisong:o78OAY2nQYa5CKBN@hearudb.7t1d8gs.mongodb.net/?retryWrites=true&w=majority&appName=hearuDB")
collection = client["hearu_data"]["user_analysis"]

@router.get("/result")
async def get_result(email: str = Query(...)):
    print(f"🔍 FastAPI received email: {email}")

    regex = Regex(f"^{email.strip()}$", "i")

    latest = collection.find_one({"email": regex}, sort=[("timestamp", -1)])

    if not latest:
        print("❌ No record found in MongoDB.")
        return JSONResponse(status_code=404, content={"error": "No record found"})

    latest["_id"] = str(latest["_id"])
    latest["timestamp"] = latest["timestamp"].isoformat()
    
    print("✅ Record found:", latest)
    return JSONResponse(content=latest)
