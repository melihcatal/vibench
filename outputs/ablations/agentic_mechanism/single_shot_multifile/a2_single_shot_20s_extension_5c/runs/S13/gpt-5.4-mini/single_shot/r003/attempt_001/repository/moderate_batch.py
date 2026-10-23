from typing import Any, Dict, List

from safety_client import ModerationProviderClient, load_safety_config
from safety_models import normalize_batch_moderation_result


def moderate_batch(messages: List[str], user_id: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = load_safety_config()
    client = ModerationProviderClient(config)
    result = client.moderate_batch(messages=messages, user_id=user_id, metadata=metadata or {})
    return normalize_batch_moderation_result(result)
