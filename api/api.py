import uvicorn 
from fastapi import FastAPI
from controller import chat

app = FastAPI()
app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
