from fastapi import APIRouter
from data.dataloader import load_data
from pipeline.ingest import convert_data_to_vector
import asyncio

router = APIRouter()
    
@router.get("/ingest")
def ingest():
    asyncio.run(convert_data_to_vector(load_data()))


@router.get("/chunk")
def chunk():
    chunk(load_data())