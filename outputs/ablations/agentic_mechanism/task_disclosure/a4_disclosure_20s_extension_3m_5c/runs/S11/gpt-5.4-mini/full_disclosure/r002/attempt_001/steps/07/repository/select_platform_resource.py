from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class PlatformResource:
    provider: str
    resource_id: str
    resource_type: str
    model: str
    metadata: Dict[str, Any]


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _resolve_model_id(preferred: Optional[str], fallback: str = "gpt-4.1-mini") -> str:
    return preferred or os.environ.get("OPENAI_MODEL", fallback)


def select_platform_resource(
    resource_id: Optional[str] = None,
    resource_type: str = "model",
    model: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> PlatformResource:
    resolved_model = _resolve_model_id(model)
    resolved_resource_id = resource_id or os.environ.get("OPENAI_MODEL_ID") or resolved_model
    resolved_resource_type = resource_type or "model"
    resolved_metadata = dict(metadata or {})
    resolved_metadata.setdefault("provider", "openai")
    resolved_metadata.setdefault("model", resolved_model)
    if not resolved_resource_id:
        response = _client().models.retrieve(resolved_model)
        resolved_resource_id = getattr(response, "id", resolved_model)
        resolved_metadata["platform_response"] = response
    return PlatformResource(
        provider="openai",
        resource_id=resolved_resource_id,
        resource_type=resolved_resource_type,
        model=resolved_model,
        metadata=resolved_metadata,
    )
