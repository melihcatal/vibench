import os
from typing import Optional


_OPENAI_RESOURCE_ALIASES = {
    "gpt-5.4-mini": "openai/gpt-5.4-mini",
    "gpt-5.4": "openai/gpt-5.4-mini",
    "openai/gpt-5.4-mini": "openai/gpt-5.4-mini",
}


def select_platform_resource(resource: Optional[str] = None) -> str:
    candidate = (resource or os.getenv("OPENAI_MODEL") or os.getenv("OPENAI_DEPLOYMENT") or "").strip()
    if not candidate:
        return "openai/gpt-5.4-mini"
    if candidate in _OPENAI_RESOURCE_ALIASES:
        return _OPENAI_RESOURCE_ALIASES[candidate]
    if candidate.startswith("openai/"):
        return candidate
    return f"openai/{candidate}"
