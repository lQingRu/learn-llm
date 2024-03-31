from typing import List
from elasticsearch import  AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from schema.data import TelegramChatMessage
from config.constants import ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL, ES_CONVERSATION_INDEX, HUGGINGFACE_EMBEDDING_MODEL,ELASTICSEARCH_SSL_VERIFY
from model.huggingface_model import get_embedding_model
from loguru import logger
import json
import ast

# TODO: Relook at async_bulk - error "elastic_transport.ConnectionTimeout: Connection timed out" 
async def ingest_bulk_data(index_name: str, data: List):
    es_client = AsyncElasticsearch(basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD), verify_certs=ast.literal_eval(ELASTICSEARCH_SSL_VERIFY),hosts=ELASTICSEARCH_URL)
    logger.info("Ingesting data async now...")
    await async_bulk(es_client, gen_index_bulk(index_name, data))
        
def gen_index_bulk(index_name: str, data: List):
    for doc in data:
        yield {
          "_index": index_name,
          "doc": doc  
        }

def embed_document(data: List[TelegramChatMessage]):
    embeddings: List[List[float]] = []
    embedding_model =  get_embedding_model()
    for doc in data:
        try:
            embedding = embedding_model.embed_query(json.dumps(doc.__dict__))
        # Possible reasons: rate limit (~64)
        except Exception as e:
            logger.error(e)
            break
        embeddings.append(embedding[0])
    return embeddings


async def convert_data_to_vector(data: List[TelegramChatMessage]):
    embeddings = embed_document(data)
    await ingest_bulk_data(ES_CONVERSATION_INDEX, embeddings)
    