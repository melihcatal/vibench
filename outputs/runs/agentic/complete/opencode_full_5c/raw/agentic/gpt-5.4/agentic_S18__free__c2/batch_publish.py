from __future__ import annotations

from typing import Any

from google.cloud import pubsub_v1

from messaging_client import publish_request, topic_path
from messaging_models import PublishRequest


def batch_publish(messages: list[dict[str, Any]]) -> dict[str, object]:
    provider_client = pubsub_v1.PublisherClient()
    provider_topic = topic_path()
    published = []
    for item in messages:
        request = PublishRequest.from_input(
            payload=item["payload"],
            attributes=item.get("attributes"),
            ordering_key=item.get("ordering_key"),
            message_id=item.get("message_id"),
        )
        provider_message_id = publish_request(request)
        published.append(
            {
                "message_id": request.message_id,
                "provider_message_id": provider_message_id,
                "attributes": request.attributes,
            }
        )
    return {
        "provider": "google-cloud-pubsub",
        "topic": provider_topic,
        "provider_client": provider_client.__class__.__name__,
        "count": len(published),
        "messages": published,
    }
