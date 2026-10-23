from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from messaging_client import publisher_client, topic_path
from messaging_models import EventMessage, normalize_attributes



def batch_publish(
    payloads: Iterable[Dict[str, Any]],
    base_attributes: Optional[Dict[str, Any]] = None,
    topic_id: Optional[str] = None,
    project_id: Optional[str] = None,
) -> List[Dict[str, str]]:
    client = publisher_client()
    destination = topic_path(topic_id=topic_id, project_id=project_id)
    common_attributes = normalize_attributes(base_attributes)
    results: List[Dict[str, str]] = []

    for index, payload in enumerate(payloads):
        event = EventMessage(
            payload=payload,
            attributes={**common_attributes, "batch_index": str(index)},
        )
        future = client.publish(destination, event.to_pubsub_data(), event_id=event.event_id, **event.attributes)
        results.append({"event_id": event.event_id, "message_id": future.result()})

    return results
