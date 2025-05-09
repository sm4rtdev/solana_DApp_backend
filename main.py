from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import TxLog
from db import create_db_and_tables, get_session
from datetime import datetime
from sqlmodel import Session

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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/log-tx")
async def log_tx(data: TxInput):
    with get_session() as session:
        tx = TxLog(wallet=data.wallet, signature=data.signature)
        session.add(tx)
        session.commit()
        session.refresh(tx)
        print(f"✅ Logged TX: {tx.signature} from {tx.wallet}")
        return {"success": True, "id": tx.id}
