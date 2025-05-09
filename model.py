from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TxLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    wallet: str
    signature: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
