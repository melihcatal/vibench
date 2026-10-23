from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import json


@dataclass
class CompletionRequest:
    """Request for LLM completion."""

    prompt: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.3
    max_tokens: int = 500
    stop: Optional[List[str]] = None
    system_prompt: Optional[str] = None

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})

        request = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if self.stop:
            request["stop"] = self.stop

        return request


@dataclass
class CompletionResponse:
    """Response from LLM completion."""

    text: str
    model: str
    usage: Optional[Dict[str, int]] = None
    finish_reason: Optional[str] = None

    @classmethod
    def from_openai_response(cls, response: Any) -> "CompletionResponse":
        """Create from OpenAI response object."""
        return cls(
            text=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            if response.usage
            else None,
            finish_reason=response.choices[0].finish_reason,
        )


@dataclass
class ChatMessage:
    """Single chat message."""

    role: str  # "system", "user", "assistant"
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class ChatRequest:
    """Request for chat completion."""

    messages: List[ChatMessage]
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.3
    max_tokens: int = 500

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        return {
            "model": self.model,
            "messages": [msg.to_dict() for msg in self.messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }


def normalize_text(text: str) -> str:
    """Normalize text by stripping whitespace and ensuring proper formatting."""
    return text.strip()


def parse_json_response(text: str) -> Dict[str, Any]:
    """Parse JSON from model response, handling potential formatting issues."""
    try:
        # Try direct JSON parsing
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from text
        import re

        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # If all else fails, return as plain text
        return {"text": text}


def validate_model_name(model_name: str) -> bool:
    """Validate if model name is a known OpenAI model."""
    openai_models = {
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
    }
    return model_name in openai_models


def estimate_token_count(text: str) -> int:
    """Rough estimate of token count for text."""
    # Rough approximation: 4 chars per token for English text
    return len(text) // 4
