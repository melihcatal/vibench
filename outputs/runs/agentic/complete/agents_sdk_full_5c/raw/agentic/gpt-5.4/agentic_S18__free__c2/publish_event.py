from __future__ import annotations

from typing import Any, Mapping, Optional

from google.api_core.retry import Retry

from messaging_client import publisher_client, topic_path
from messaging_models import EventMessage


DEFAULT_RETRY = Retry(initial=0.1, maximum=10.0, multiplier=2.0, deadline=30.0)


def publish_event(
    payload: Mapping[str, Any],
    *,
    attributes: Optional[Mapping[str, Any]] = None,
    topic_id: Optional[str] = None,
    project_id: Optional[str] = None,
    ordering_key: Optional[str] = None,
) -> str:
    client = publisher_client()
    message = EventMessage.from_mapping(
        payload,
        attributes=attributes,
        ordering_key=ordering_key,
    )
    future = client.publish(
        topic_path(topic_id=topic_id, project_id=project_id),
        message.to_json_bytes(),
        ordering_key=message.ordering_key or "",
        **message.attributes,
    )
    return future.result(retry=DEFAULT_RETRY)
