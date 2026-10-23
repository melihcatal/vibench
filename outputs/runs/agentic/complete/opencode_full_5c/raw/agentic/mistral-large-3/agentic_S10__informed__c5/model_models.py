from typing import List, Dict, Any, Optional, NamedTuple
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    message: Message
    delta: Optional[Message] = None


class ModelResponse(BaseModel):
    choices: List[Choice]


class ModelRequest(BaseModel):
    prompt: str
    model_family: str = "mistral"
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stream: bool = False
    messages: Optional[List[Dict[str, str]]] = None


def normalize_request(request: ModelRequest) -> Dict[str, Any]:
    """Normalize request for Mistral API."""
    model_mapping = {
        "mistral": "mistral-tiny",
        "mistral-small": "mistral-small",
        "mistral-medium": "mistral-medium",
        "mistral-large": "mistral-large-latest",
    }

    model = model_mapping.get(request.model_family, request.model_family)

    messages = request.messages or [{"role": "user", "content": request.prompt}]

    return {
        "model": model,
        "messages": messages,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "stream": request.stream,
    }


def parse_response(response: Dict[str, Any]) -> ModelResponse:
    """Parse response from Mistral API."""
    return ModelResponse(**response)


def parse_streaming_response(chunk: Dict[str, Any]) -> ModelResponse:
    """Parse streaming response chunk from Mistral API."""
    return ModelResponse(**chunk)
