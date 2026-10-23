from __future__ import annotations

from typing import Dict, Optional

from model_client import get_responses_model


MODEL_CATALOG: Dict[str, str] = {
    "chat": "gpt-4.1-mini",
    "reasoning": "o4-mini",
    "quality": "gpt-4.1",
    "fast": "gpt-4.1-nano",
}


def select_platform_resource(
    task: str = "chat", override_model: Optional[str] = None
) -> str:
    if override_model:
        return override_model
    if task in MODEL_CATALOG:
        return MODEL_CATALOG[task]
    return get_responses_model()
