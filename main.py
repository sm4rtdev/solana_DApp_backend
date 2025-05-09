from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB", "solana_dapp")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "txlogs")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TxInput(BaseModel):
    wallet: str
    signature: str


@app.post("/log-tx")
async def log_tx(data: TxInput):
    doc = {
        "wallet": data.wallet,
        "signature": data.signature,
        "created_at": datetime.utcnow()
    }
    result = await collection.insert_one(doc)
    return {"success": True, "id": str(result.inserted_id)}


@app.get("/logs")
async def get_logs():
    logs = await collection.find().to_list(100)
    for log in logs:
        log["_id"] = str(log["_id"])
    return logs
