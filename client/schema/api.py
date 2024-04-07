from pydantic import BaseModel


class PostQuestionRequestBody(BaseModel):
    prompt: str
    prompt_version: int