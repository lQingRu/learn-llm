from schema.data import TelegramChatMessage
from langchain.schema import Document

def convert_to_document(message_obj: TelegramChatMessage) -> Document:
    return Document(page_content=message_obj.message, metadata = {"sender": message_obj.sender, "timestamp": message_obj.timestamp})