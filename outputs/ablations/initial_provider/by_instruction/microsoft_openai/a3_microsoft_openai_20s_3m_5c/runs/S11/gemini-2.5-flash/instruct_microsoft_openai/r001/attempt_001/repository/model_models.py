from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class Message:
    role: str
    content: str

@dataclass
class ModelRequest:
    messages: List[Message]
    model: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 150

@dataclass
class ModelResponse:
    id: str
    model: str
    created: int
    choices: List[Dict[str, Any]]
    usage: Dict[str, Any]
    provider: str = "unknown"

def normalize_openai_response(response: Any) -> ModelResponse:
    """Normalizes an OpenAI API response into a common ModelResponse format."""
    return ModelResponse(
        id=response.id,
        model=response.model,
        created=response.created,
        choices=[choice.model_dump() for choice in response.choices],
        usage=response.usage.model_dump() if response.usage else {},
        provider="openai"
    )

