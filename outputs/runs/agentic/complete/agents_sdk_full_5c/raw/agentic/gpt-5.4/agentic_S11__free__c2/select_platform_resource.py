from __future__ import annotations

from typing import Iterable, Optional

from model_client import get_chat_deployment


PREFERRED_AZURE_OPENAI_DEPLOYMENTS = (
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1-mini",
)



def select_platform_resource(available_resources: Optional[Iterable[str]] = None) -> str:
    available = list(available_resources or [])
    configured = get_chat_deployment()
    if configured in available:
        return configured
    for candidate in PREFERRED_AZURE_OPENAI_DEPLOYMENTS:
        if candidate in available:
            return candidate
    if configured:
        return configured
    if available:
        return available[0]
    raise ValueError("No Azure OpenAI deployment resource could be resolved")
