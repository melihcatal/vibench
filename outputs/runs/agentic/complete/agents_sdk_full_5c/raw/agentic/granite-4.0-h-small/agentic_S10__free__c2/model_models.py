from typing import Any, Dict, List, Optional

class LLMRequest:
    """Encapsulation of a request sent to a hosted LLM provider."""
    def __init__(self, model: str, messages: List[Dict[str, Any]], **kwargs):
        self.model = model
        self.messages = messages
        self.temperature = kwargs.get("temperature", 0.2)
        self.max_tokens = kwargs.get("max_tokens", 256)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }


class LLMResponse:
    """Container for the provider‑agnostic expected response shape."""
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw

    @property
    def choices(self) -> List[Dict[str, Any]]:
        return self.raw.get("choices", [])

    @property
    def usage(self) -> Optional[Dict[str, Any]]:
        return self.raw.get("usage")

    @property
    def error(self) -> Optional[Dict[str, Any]]:
        return self.raw.get("error")


def normalize_response(raw: Dict[str, Any]) -> LLMResponse:
    """Convert provider‑specific raw dict to a uniform LLMResponse."""
    # If the provider returns a top‑level error, re‑raise or attach it.
    if raw.get("error"):
        raise RuntimeError(f"LLM error: {raw['error']['message']}")
    return LLMResponse(raw)