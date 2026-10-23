from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    system_prompt: Optional[str] = None
    messages: List[str] = []
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 1000


class ChatResponse(BaseModel):
    content: str
    raw_response: Dict[str, Any]


class StreamResponseChunk(BaseModel):
    content: str
    raw_response: Dict[str, Any]


def parse_usage_metadata(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses Azure AI Inference usage metadata from raw response.
    """
    return {
        "prompt_tokens": raw_response.get("usage", {}).get("prompt_tokens", 0),
        "completion_tokens": raw_response.get("usage", {}).get("completion_tokens", 0),
        "total_tokens": raw_response.get("usage", {}).get("total_tokens", 0),
    }
