from pydantic import BaseModel
from typing import Optional, Dict, Any


class WatsonXRequest(BaseModel):
    prompt: str
    model_id: Optional[str] = "ibm/granite-13b-chat-v2"
    params: Optional[Dict[str, Any]] = None


class WatsonXStreamRequest(BaseModel):
    prompt: str
    model_id: Optional[str] = "ibm/granite-13b-chat-v2"
    params: Optional[Dict[str, Any]] = None


class WatsonXResponse(BaseModel):
    generated_text: str
    usage: Dict[str, Any]
    model_id: str
    created_at: Optional[str] = None