from loguru import logger
from langchain import PromptTemplate

def get_system_prompt(version: int) -> str:
    version_1 = """
            You are a chat interpreter. With the following chat messages in "Context", please answer the following question in "Question".
            
            Context:
            {context}
            
            Question:
            {question}
            """
    
    match version:
        case 1:
            return version_1
        case default:
            logger.error("No such prompt version available, defaulting to version 1. Only - [1]")
            return version_1
        
# TODO: Different versions of prompts
def build_prompt(question: str, prompt_version: int):
    template = get_system_prompt(prompt_version)
    prompt = PromptTemplate(input_variables=["question", "context"], template=template)
    

    