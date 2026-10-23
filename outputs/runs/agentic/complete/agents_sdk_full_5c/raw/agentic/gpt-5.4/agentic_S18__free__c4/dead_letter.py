from __future__ import annotations

from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_config, get_publisher_client
from messaging_models import json_bytes


GOOGLE_PUBSUB_PROVIDER = "google-cloud-pubsub"


def send_to_dead_letter(original_payload: Dict[str, Any], reason: str, ack_id: str = "") -> str:
    config = get_config()
    publisher: pubsub_v1.PublisherClient = get_publisher_client()

    envelope = {
        "reason": reason,
        "ack_id": ack_id,
        "original_payload": original_payload,
    }

    future = publisher.publish(
        config.dead_letter_topic_path,
        json_bytes(envelope),
        dead_letter_reason=reason,
        original_ack_id=ack_id,
    )
    return future.result()
