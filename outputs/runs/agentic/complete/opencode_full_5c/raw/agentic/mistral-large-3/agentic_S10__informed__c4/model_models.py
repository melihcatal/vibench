from typing import Dict, Any, Optional, Iterator
from pydantic import BaseModel


class LLMRequest(BaseModel):
    """
    Represents a request to an LLM.
    """

    model_identifier: str
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.7
    stream: bool = False
    extra_params: Dict[str, Any] = {}


class LLMResponse(BaseModel):
    """
    Represents a response from an LLM.
    """

    text: str
    model_identifier: str
    usage: Dict[str, Any] = {}


class LLMResponseChunk(BaseModel):
    """
    Represents a chunk of a streaming response from an LLM.
    """

    text: str
    model_identifier: str
