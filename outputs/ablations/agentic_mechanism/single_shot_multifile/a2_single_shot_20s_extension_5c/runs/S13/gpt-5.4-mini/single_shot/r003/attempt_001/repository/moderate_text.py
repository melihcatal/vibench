import os
from typing import Any, Dict

from safety_client import ModerationProviderClient, load_safety_config
from safety_models import normalize_moderation_result


def moderate_text(text: str, user_id: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = load_safety_config()
    client = ModerationProviderClient(config)
    result = client.moderate_text(text=text, user_id=user_id, metadata=metadata or {})
    return normalize_moderation_result(result)
