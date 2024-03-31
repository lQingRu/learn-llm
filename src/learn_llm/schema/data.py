from pydantic import BaseModel

class TelegramChatMessage(BaseModel):
    sender: str
    message: str # Mainly for ease to ingest into vectorstores via Langchain
    timestamp: str
    