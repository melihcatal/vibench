from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from typing import Union


@dataclass
class ChatRequest:
    messages: List[str]
    system_message: Optional[str] = None
    data_sources: Optional[List[Dict[str, Any]]] = None


@dataclass
class ChatResponse:
    id: str
    model: str
    content: str
    usage: Dict[str, int]
    raw_response: Any


@dataclass
class StreamChunk:
    id: str
    model: str
    content: str
    raw_chunk: Any


def normalize_response(response: Dict[str, Any]) -> ChatResponse:
    """
    Normalizes Azure AI Inference response into a standardized format.
    """
    return ChatResponse(
        id=response.get("id", ""),
        model=response.get("model", ""),
        content=response.get("content", ""),
        usage=response.get("usage", {}),
        raw_response=response,
    )
