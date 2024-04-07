from datetime import datetime
from typing import List
from pydantic import BaseModel


class EmbeddingConvo(BaseModel):
    embedding: List[List[float]] = []
    #embedding: str
    doc: str
    ingest_timestamp: datetime