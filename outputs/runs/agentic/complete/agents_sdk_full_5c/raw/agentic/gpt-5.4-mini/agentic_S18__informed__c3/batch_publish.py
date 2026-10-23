from __future__ import annotations

from typing import Any, Dict, Iterable, List

from messaging_client import get_pubsub_settings, publisher_client, topic_path, serialize_json
from messaging_models import BatchPublishItem, PublishResponse


def publish_batch(items: Iterable[BatchPublishItem]) -> List[PublishResponse]:
    settings = get_pubsub_settings()
    topic = topic_path(settings.project_id, settings.topic_id)
    client = publisher_client()
    futures = []
    responses: List[PublishResponse] = []
    for item in items:
        attrs = item.normalized_attributes()
        futures.append((attrs, client.publish(topic, serialize_json({"event_id": item.event_id, "payload": item.payload}), **attrs)))
    for attrs, future in futures:
        responses.append(PublishResponse(message_id=future.result(), topic=topic, attributes=attrs))
    return responses
