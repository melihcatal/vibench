"""
Define local request, response, and normalization helpers for Hosted LLM
Inference and Model-Family Selection with Anthropic Claude models.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import json


@dataclass
class LLMRequest:
    """Standardized request payload for hosted LLM calls."""
    text: str
    system_prompt: Optional[str] = None
    model_id: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.7
    context: Optional[str] = None
    format_instructions: Optional[str] = None

    def to_anthropic_messages(self) -> Dict[str, Any]:
        """Convert to Anthropic Messages API request format."""
        messages = [{"role": "user", "content": self.text}]
        request_data = {
            "model": self.model_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": messages,
        }
        if self.system_prompt:
            request_data["system"] = self.system_prompt
        return request_data


@dataclass
class LLMResponse:
    """Standardized response from a hosted LLM call."""
    text: str = ""
    model: str = ""
    stop_reason: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    raw_response: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize response to dictionary."""
        return {
            "text": self.text,
            "model": self.model,
            "stop_reason": self.stop_reason,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
        }


@dataclass
class ExtractedJSON:
    """Container for JSON extracted from LLM output."""
    data: Dict[str, Any] = field(default_factory=dict)
    raw_text: str = ""
    parse_error: Optional[str] = None

    @classmethod
    def from_text(cls, text: str) -> "ExtractedJSON":
        """Attempt to parse JSON from LLM response text."""
        cleaned = text.strip()
        # Try to find JSON block
        if "```json" in cleaned:
            start = cleaned.index("```json") + len("```json")
            end = cleaned.index("```", start)
            cleaned = cleaned[start:end].strip()
        elif "```" in cleaned:
            start = cleaned.index("```") + len("```")
            end = cleaned.index("```", start)
            cleaned = cleaned[start:end].strip()

        try:
            data = json.loads(cleaned)
            return cls(data=data, raw_text=text)
        except json.JSONDecodeError as e:
            return cls(raw_text=text, parse_error=str(e))


SUPPORTED_CLAUDE_MODELS = {
    "claude-3-5-sonnet-20241022": {"family": "claude", "max_tokens": 8192},
    "claude-3-opus-20240229": {"family": "claude", "max_tokens": 4096},
    "claude-3-haiku-20240307": {"family": "claude", "max_tokens": 4096},
}


def validate_model_id(model_id: str) -> bool:
    """Check if a model ID is a supported Claude model."""
    return model_id in SUPPORTED_CLAUDE_MODELS


def get_model_family(model_id: str) -> Optional[str]:
    """Return the model family for a given model ID."""
    if model_id in SUPPORTED_CLAUDE_MODELS:
        return SUPPORTED_CLAUDE_MODELS[model_id]["family"]
    return None
