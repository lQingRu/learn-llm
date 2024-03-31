from typing import List, Optional
from pydantic import Field
from config.constants import HUGGINGFACEHUB_API_TOKEN,HUGGINGFACE_EMBEDDING_MODEL, HUGGINGFACE_LLM_MODEL
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

class HuggingFaceLLMModel():
    model_name: str = Field(None, alias='model_name')
    api_key: str = Field(None, alias='api_key')

    # all the optional arguments
    backend:        Optional[str]   = 'llama'
    temp:           Optional[float] = 0.7
    n_batch:        Optional[int]   = 8
    max_tokens:     Optional[int]   = 200
    stop: Optional[List[str]] = None
    
    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = HUGGINGFACEHUB_API_TOKEN

    @property
    def _get_model_default_parameters(self):
        return {
            "max_tokens": self.max_tokens,
            "temp": self.temp,
            "stop": self.stop
        }   
    
    @property
    def _get_model(self):
        llm = HuggingFaceEndpoint(repo_id=self.model_name, temperature = self.temp, token = self.api_key, max_new_tokens= self.max_tokens, stop=self.stop)
        return llm      

class HuggingFaceEmbeddingModel():
    model_name: str = Field(None, alias='model_name')
    api_key: str = Field(None, alias='api_key')

    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = HUGGINGFACEHUB_API_TOKEN
        
    @property
    def _get_model(self) -> HuggingFaceInferenceAPIEmbeddings:
        return HuggingFaceInferenceAPIEmbeddings(api_key=self.api_key, model_name=self.model_name)
    
def get_embedding_model():
    return HuggingFaceEmbeddingModel(model_name=HUGGINGFACE_EMBEDDING_MODEL)._get_model

def get_llm_model():
    return HuggingFaceLLMModel(model_name=HUGGINGFACE_EMBEDDING_MODEL)._get_model