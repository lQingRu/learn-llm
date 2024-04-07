from pipeline.model.huggingface_model import get_embedding_model
from loguru import logger
from elasticsearch import  Elasticsearch
import json
import ast

from pipeline.config.constants import ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL, ES_CONVERSATION_INDEX, ELASTICSEARCH_SSL_VERIFY

es_client = Elasticsearch(basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD), verify_certs=ast.literal_eval(ELASTICSEARCH_SSL_VERIFY),hosts=ELASTICSEARCH_URL, timeout=5)

def retrieve_context(question: str):
    # Get top 10 convos
    response = vector_search(question)
    
    # Re-rank
    
    # Return context
    
    
    
def vector_search(question: str):
    embedding_model = get_embedding_model()
    embedding = embedding_model.embed_query(question)[0]
    if embedding is not None:
        response = es_client.search(
            index = ES_CONVERSATION_INDEX,
            knn= {
                "field": "embedding",
                "query_vector": embedding,
                "k": 10,
                "num_candidates": 100
            }
        )
        return response
    else:
        return None