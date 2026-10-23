from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class ModelRequest(BaseModel):
    """Request model for Azure AI Inference."""

    system_prompt: str
    user_prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000


class ModelResponse(BaseModel):
    """Response model for Azure AI Inference."""

    id: str
    content: str
    finish_reason: str
    usage: Dict[str, int]
    model: str
    system_fingerprint: Optional[str] = None


class StreamChunk(BaseModel):
    """Streaming chunk model for Azure AI Inference."""

    id: str
    content: str
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None


class PlatformMetadata(BaseModel):
    """Metadata from Azure AI Inference platform."""

    model: str
    deployment_id: str
    usage: Dict[str, int]
    system_fingerprint: Optional[str] = None
    invocation_id: Optional[str] = None
