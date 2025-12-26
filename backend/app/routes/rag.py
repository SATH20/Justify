from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_engine import RAGEngine

router = APIRouter()
rag_engine = RAGEngine()

class RAGRequest(BaseModel):
    query: str

@router.post("/rag")
async def rag_endpoint(request: RAGRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query field cannot be empty.")
    results = rag_engine.retrieve(request.query)
    return {"results": results}
