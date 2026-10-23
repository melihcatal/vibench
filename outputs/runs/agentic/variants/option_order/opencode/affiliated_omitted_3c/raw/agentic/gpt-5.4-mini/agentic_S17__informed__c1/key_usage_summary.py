from typing import Any, Dict, List

from security_models import normalize_text


def summarize_key_usage(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    cleaned = []
    for event in events:
        cleaned.append({k: normalize_text(str(v)) if isinstance(v, str) else v for k, v in event.items()})
    return {"provider": "aws-kms", "event_count": len(cleaned), "events": cleaned}
