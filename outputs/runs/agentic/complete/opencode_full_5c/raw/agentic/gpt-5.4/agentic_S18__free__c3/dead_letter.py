from __future__ import annotations

from typing import Any, Dict

from messaging_client import pubsub_config, pubsub_post, topic_path
from messaging_models import MessagePayload, PublishResult, encode_message_data


def dead_letter(message: Dict[str, Any], reason: str) -> PublishResult:
    config = pubsub_config()
    dead_topic = topic_path(config["dead_letter_topic_id"])
    payload = MessagePayload.from_dict(message)
    payload.attributes = {
        **payload.attributes,
        "dead_letter_reason": reason,
        "delivery": "dead-letter",
    }
    response = pubsub_post(
        f"{dead_topic}:publish",
        {
            "messages": [
                {
                    "data": encode_message_data(
                        {
                            "message_id": payload.message_id,
                            "event_type": payload.event_type,
                            "source": payload.source,
                            "data": payload.data,
                            "reason": reason,
                        }
                    ),
                    "attributes": payload.attributes,
                }
            ]
        },
    )
    return PublishResult(
        provider="google_pubsub",
        destination=dead_topic,
        message_ids=[str(message_id) for message_id in response.get("messageIds", [])],
    )
