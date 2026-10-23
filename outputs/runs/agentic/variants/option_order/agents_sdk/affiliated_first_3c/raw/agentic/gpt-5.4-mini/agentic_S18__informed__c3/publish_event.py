from __future__ import annotations

import json
from typing import Any, Dict

from messaging_client import publish_json
from messaging_models import PublishRequest, normalize_attributes


def publish_event(payload: Any, topic: str | None = None, attributes: Dict[str, str] | None = None) -> str:
    request = PublishRequest(
        topic=topic or "",
        payload=payload if isinstance(payload, (dict, list)) else json.loads(payload) if isinstance(payload, str) else payload,
        attributes=normalize_attributes(attributes),
    )
    return publish_json(request)
