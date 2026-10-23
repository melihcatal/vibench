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
    client: Any
    raw: Dict[str, Any]


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value else default


def _pick_resource_identifier() -> str:
    for key in (
        "OPENAI_MODEL",
        "OPENAI_DEPLOYMENT",
        "OPENAI_INFERENCE_PROFILE",
        "OPENAI_RESOURCE_ID",
    ):
        value = _env(key)
        if value:
            return value
    return "gpt-5.4-mini"


def _resource_type(identifier: str) -> str:
    lowered = identifier.lower()
    if lowered.startswith("fp_"):
        return "fine_tuned_model"
    if "/deployments/" in lowered or lowered.startswith("deployment:"):
        return "deployment"
    if lowered.startswith("ip_") or "inference" in lowered:
        return "inference_profile"
    return "model"


def select_platform_resource(resource_id: Optional[str] = None) -> PlatformResource:
    identifier = resource_id or _pick_resource_identifier()
    client = OpenAI(api_key=_env("OPENAI_API_KEY"))
    resource_type = _resource_type(identifier)
    raw: Dict[str, Any] = {"provider": "openai", "resource_id": identifier, "resource_type": resource_type}
    return PlatformResource(provider="openai", resource_id=identifier, resource_type=resource_type, client=client, raw=raw)
