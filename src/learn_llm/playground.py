import uvicorn 
from fastapi import FastAPI
from controller import pipeline

app = FastAPI()
app.include_router(pipeline.router)
    
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
