from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7
    system_prompt: Optional[str] = None


@dataclass
class LLMResponse:
    content: str
    usage: Optional[Dict[str, int]] = None
    finished_reason: Optional[str] = None


def normalize_response(raw: Any) -> LLMResponse:
    """Convert provider-specific response to a unified LLMResponse."""
    if isinstance(raw, dict) and "choices" in raw:
        # openai / gpt format
        return LLMResponse(
            content=raw["choices"][0]["message"]["content"],
            usage=raw.get("usage"),
            finished_reason=raw.get("usage", {}).get("finish_reason"),
        )
    # Placeholder for other providers
    return LLMResponse(content=str(raw))
