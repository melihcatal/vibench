from __future__ import annotations

from typing import Any

from google.cloud import pubsub_v1

from messaging_client import publish_request, topic_path
from messaging_models import PublishRequest


def publish_event(
    payload: dict[str, Any] | str, attributes: dict[str, Any] | None = None
) -> dict[str, str]:
    request = PublishRequest.from_input(payload=payload, attributes=attributes)
    provider_client = pubsub_v1.PublisherClient()
    provider_topic = topic_path()
    published_provider_id = publish_request(request)
    return {
        "provider": "google-cloud-pubsub",
        "topic": provider_topic,
        "provider_client": provider_client.__class__.__name__,
        "message_id": request.message_id,
        "provider_message_id": published_provider_id,
    }
