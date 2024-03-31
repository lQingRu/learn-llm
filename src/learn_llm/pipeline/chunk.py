
from typing import List
from model.huggingface_model import get_embedding_model
from schema.data import TelegramChatMessage
from langchain_experimental.text_splitter import SemanticChunker
import json

def chunk(data: List[TelegramChatMessage]):
    embedding_model = get_embedding_model()
    text_splitter = SemanticChunker(embedding_model)
    list_of_str_data = list(map(lambda obj: (json.dumps(obj.__dict__)),data))
    documents = text_splitter.create_documents([list_of_str_data])
    print(documents[0])