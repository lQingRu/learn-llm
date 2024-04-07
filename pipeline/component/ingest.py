from datetime import datetime
from typing import List
import pytz
from elasticsearch import  Elasticsearch
from elasticsearch.helpers import bulk
from schema.esdata import EmbeddingConvo
from schema.data import TelegramChatMessage
from config.constants import ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL, ES_CONVERSATION_INDEX, ELASTICSEARCH_SSL_VERIFY
from model.huggingface_model import get_embedding_model
from loguru import logger
import json
import ast

es_client = Elasticsearch(basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD), verify_certs=ast.literal_eval(ELASTICSEARCH_SSL_VERIFY),hosts=ELASTICSEARCH_URL, timeout=5)

def ingest_bulk_data(index_name: str, data: List[EmbeddingConvo]):
    es_data = list(map(lambda obj: convert_data_to_es_schema(obj),data))
    bulk(es_client, es_data, index = index_name)

def convert_data_to_es_schema(doc: EmbeddingConvo):
    return {
        "doc": doc.doc,
        "ingest_timestamp": doc.ingest_timestamp,
        "embedding": doc.embedding
    }

def embed_document(data: List[TelegramChatMessage]) -> List[EmbeddingConvo]:
    es_docs: List[EmbeddingConvo] = []
    embedding_model =  get_embedding_model()
    for doc in data:
        try:
            embedding = embedding_model.embed_query(json.dumps(doc.__dict__))[0]
            #embedding = json.dumps(doc.__dict__)
            embedding_convo =EmbeddingConvo(embedding=embedding, doc=json.dumps(doc.__dict__), ingest_timestamp=datetime.now(tz=pytz.timezone('GMT')))
        # Possible reasons: rate limit (~64)
        except Exception as e:
            logger.error(e)
            break
        es_docs.append(embedding_convo)
    return es_docs


def convert_data_to_vector(data: List[TelegramChatMessage]):
    batch_size = 10
    current_index = 0
    logger.debug(f"Converting and Ingesting data async now in batches of {batch_size}...")
    while current_index < len(data):
        logger.debug(f"Currently processing: Index of {current_index}")
        batch_data =  data[current_index: current_index+batch_size]
        embedded_convo = embed_document(batch_data)
        ingest_bulk_data(ES_CONVERSATION_INDEX, embedded_convo)
        current_index+=batch_size
    es_client.close()    