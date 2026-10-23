from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ModelRequest:
    prompt: str
    system_instruction: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 512


@dataclass
class NormalizedModelResponse:
    text: str
    resource_name: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw_response: Optional[Any] = None


def normalize_vertex_response(response: Any) -> NormalizedModelResponse:
    text = ""
    if hasattr(response, "text") and response.text:
        text = response.text
    else:
        candidates = getattr(response, "candidates", None) or []
        if candidates:
            parts = getattr(candidates[0], "content", None)
            if parts and getattr(parts, "parts", None):
                text = "".join(getattr(part, "text", "") for part in parts.parts)
    usage = None
    if hasattr(response, "usage_metadata"):
        usage = getattr(response, "usage_metadata")
    resource_name = getattr(response, "name", None) or getattr(response, "model_version", None)
    return NormalizedModelResponse(text=text, resource_name=resource_name, usage=usage, raw_response=response)
