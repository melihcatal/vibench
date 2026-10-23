from __future__ import annotations

from typing import Dict, Optional

from model_client import OPENAI_DEFAULT_MODEL, get_openai_client


def select_platform_resource(preferred_model: Optional[str] = None) -> Dict[str, str]:
    client = get_openai_client()
    model_id = preferred_model or OPENAI_DEFAULT_MODEL
    model = client.models.retrieve(model_id)
    return {
        "provider": "openai",
        "resource_type": "model",
        "resource_id": model.id,
        "selected_model": model.id,
    }
