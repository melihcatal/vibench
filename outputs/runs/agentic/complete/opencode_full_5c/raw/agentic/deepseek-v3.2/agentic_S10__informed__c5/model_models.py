from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ModelFamily(Enum):
    """Supported model families."""

    GPT = "gpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    MISTRAL = "mistral"
    LLAMA = "llama"


@dataclass
class ChatMessage:
    """A chat message with role and content."""

    role: str  # "system", "user", "assistant"
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class CompletionRequest:
    """Request for model completion."""

    messages: List[ChatMessage]
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        return {
            "model": self.model,
            "messages": [msg.to_dict() for msg in self.messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": self.stream,
        }


@dataclass
class CompletionResponse:
    """Response from model completion."""

    content: str
    model: str
    usage: Dict[str, int]
    raw_response: Optional[Any] = None

    @classmethod
    def from_openai_response(cls, response: Any) -> "CompletionResponse":
        """Create from OpenAI response object."""
        return cls(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            raw_response=response,
        )


def normalize_text_for_model(text: str, max_length: Optional[int] = None) -> str:
    """Normalize text for model input."""
    text = text.strip()
    if max_length and len(text) > max_length:
        text = text[:max_length] + "..."
    return text


def parse_json_response(text: str) -> Dict[str, Any]:
    """Parse JSON from model response, handling common formatting issues."""
    import json
    import re

    text = text.strip()

    # Try to extract JSON if wrapped in markdown code blocks
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if json_match:
        text = json_match.group(1).strip()

    # Try to find JSON object
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        text = json_match.group(0)

    return json.loads(text)


def estimate_token_count(text: str) -> int:
    """Rough estimate of token count for OpenAI models."""
    # Rough approximation: 1 token ≈ 4 characters for English text
    return len(text) // 4
