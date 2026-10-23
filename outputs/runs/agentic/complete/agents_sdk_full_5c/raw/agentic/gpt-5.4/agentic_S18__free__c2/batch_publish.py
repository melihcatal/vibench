from __future__ import annotations

from typing import Any, Iterable, List, Mapping, Optional

from messaging_client import publisher_client, topic_path
from messaging_models import build_batch


def publish_batch(
    messages: Iterable[Mapping[str, Any]],
    *,
    topic_id: Optional[str] = None,
    project_id: Optional[str] = None,
) -> List[str]:
    client = publisher_client()
    destination = topic_path(topic_id=topic_id, project_id=project_id)
    futures = []
    for item in build_batch(messages):
        publish_attributes = dict(item.attributes)
        if item.message_id:
            publish_attributes.setdefault("client_message_id", item.message_id)
        futures.append(
            client.publish(
                destination,
                item.to_json_bytes(),
                ordering_key=item.ordering_key or "",
                **publish_attributes,
            )
        )
    return [future.result() for future in futures]
