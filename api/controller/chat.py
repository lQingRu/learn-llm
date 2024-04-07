from fastapi import APIRouter
from schema.chatapi import PostQuestionRequestBody

router = APIRouter()
@router.post("/ask")
def ask(request_body: PostQuestionRequestBody):
    print (f"asking...{request_body.prompt} with version {request_body.prompt_version}")
