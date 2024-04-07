from pydantic import BaseModel

class TelegramChatMessage(BaseModel):
    sender: str
    message: str
    timestamp: str
    