
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.main import main as process_query  # ✅ your YouTube RAG logic

router = APIRouter()

class QueryRequest(BaseModel):
    youtube_url: str
    query: str

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        result = process_query(request.youtube_url, request.query)
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})



