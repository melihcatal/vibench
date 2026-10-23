from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import json


@dataclass
class ModelRequest:
    """Request for model inference."""

    prompt: str
    system_message: Optional[str] = None
    max_tokens: int = 1000
    temperature: float = 0.7
    model: str = "gpt-3.5-turbo"
    stream: bool = False


@dataclass
class ModelResponse:
    """Response from model inference."""

    text: str
    raw_response: Optional[Any] = None
    model_used: str = ""
    tokens_used: Optional[int] = None


@dataclass
class ChatMessage:
    """Chat message for conversation."""

    role: str  # "system", "user", "assistant"
    content: str


def parse_json_response(response_text: str) -> Dict[str, Any]:
    """Parse JSON response from model."""
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON if wrapped in other text
        import re

        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        raise ValueError(
            f"Could not parse JSON from response: {response_text[:100]}..."
        )


def validate_request(request: ModelRequest) -> bool:
    """Validate model request."""
    if not request.prompt or not request.prompt.strip():
        return False
    if request.temperature < 0 or request.temperature > 2:
        return False
    if request.max_tokens <= 0:
        return False
    return True


def build_chat_messages(request: ModelRequest) -> List[Dict[str, str]]:
    """Build chat messages from request."""
    messages = []
    if request.system_message:
        messages.append({"role": "system", "content": request.system_message})
    messages.append({"role": "user", "content": request.prompt})
    return messages
