from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.legal_agent import LegalAgent

router = APIRouter()
agent = LegalAgent()


class AgentRequest(BaseModel):
    query: str
    session_id: str


@router.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    query = request.query.strip()
    session_id = request.session_id.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query field cannot be empty.")
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID cannot be empty.")
    result = agent.decide_and_act(query, session_id)
    return result
