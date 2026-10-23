from __future__ import annotations

from google.cloud import pubsub_v1

from messaging_client import (
    build_dead_letter_payload,
    get_dead_letter_topic_name,
    publish_request,
    topic_path,
)
from messaging_models import ConsumedMessage


def send_to_dead_letter(message: ConsumedMessage, reason: str) -> dict[str, str]:
    provider_client = pubsub_v1.PublisherClient()
    dead_letter_topic_name = get_dead_letter_topic_name()
    provider_topic = topic_path(dead_letter_topic_name)
    request = build_dead_letter_payload(message, reason)
    provider_message_id = publish_request(request, topic_name=dead_letter_topic_name)
    return {
        "provider": "google-cloud-pubsub",
        "dead_letter_topic": provider_topic,
        "provider_client": provider_client.__class__.__name__,
        "original_message_id": message.message_id,
        "provider_message_id": provider_message_id,
    }
