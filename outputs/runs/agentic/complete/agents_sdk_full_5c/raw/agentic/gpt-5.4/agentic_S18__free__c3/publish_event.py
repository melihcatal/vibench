from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import publisher_client, topic_path
from messaging_models import EventMessage, normalize_attributes



def publish_event(
    payload: Dict[str, Any],
    attributes: Optional[Dict[str, Any]] = None,
    ordering_key: Optional[str] = None,
    topic_id: Optional[str] = None,
    project_id: Optional[str] = None,
) -> str:
    client = publisher_client()
    event = EventMessage(
        payload=payload,
        attributes=normalize_attributes(attributes),
        ordering_key=ordering_key,
    )
    future = client.publish(
        topic_path(topic_id=topic_id, project_id=project_id),
        event.to_pubsub_data(),
        **event.attributes,
    )
    return future.result()
