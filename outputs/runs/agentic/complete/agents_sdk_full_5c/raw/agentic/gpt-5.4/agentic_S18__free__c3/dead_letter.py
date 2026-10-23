from __future__ import annotations

from typing import Any, Dict, Optional
import json

from messaging_client import dead_letter_topic_path, publisher_client
from messaging_models import normalize_attributes



def send_to_dead_letter(
    failed_payload: Dict[str, Any],
    reason: str,
    attributes: Optional[Dict[str, Any]] = None,
    dead_letter_topic_id: Optional[str] = None,
    project_id: Optional[str] = None,
) -> str:
    client = publisher_client()
    merged_attributes = normalize_attributes(attributes)
    merged_attributes["dead_letter_reason"] = reason
    body = json.dumps(
        {"failed_payload": failed_payload, "reason": reason},
        separators=(",", ":"),
    ).encode("utf-8")
    future = client.publish(
        dead_letter_topic_path(topic_id=dead_letter_topic_id, project_id=project_id),
        body,
        **merged_attributes,
    )
    return future.result()
