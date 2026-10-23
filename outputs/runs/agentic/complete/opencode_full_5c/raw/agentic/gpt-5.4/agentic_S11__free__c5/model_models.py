from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ModelRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.2
    locale: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformResource:
    inference_profile_arn: Optional[str] = None
    region_name: Optional[str] = None
    model_id: Optional[str] = None


@dataclass
class ModelResponse:
    text: str
    model_id: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw_response: Any = None


def build_messages(request: ModelRequest) -> List[Dict[str, Any]]:
    return [{"role": "user", "content": [{"text": request.prompt}]}]


def normalize_text_blocks(blocks: Iterable[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for block in blocks:
        text = block.get("text")
        if text:
            parts.append(text)
    return "".join(parts)


def normalize_converse_output(response: Dict[str, Any]) -> str:
    output = response.get("output", {})
    message = output.get("message", {})
    content = message.get("content", [])
    return normalize_text_blocks(content)


def extract_usage(response: Dict[str, Any]) -> Dict[str, Any]:
    usage = response.get("usage", {}) or {}
    return {
        "input_tokens": usage.get("inputTokens"),
        "output_tokens": usage.get("outputTokens"),
        "total_tokens": usage.get("totalTokens"),
    }
