from __future__ import annotations

from typing import Any, Dict

from messaging_client import pubsub_post, topic_path
from messaging_models import MessagePayload, PublishResult, encode_message_data


def publish_event(event: Dict[str, Any]) -> PublishResult:
    payload = MessagePayload.from_dict(event)
    response = pubsub_post(
        f"{topic_path()}:publish",
        {
            "messages": [
                {
                    "data": encode_message_data(
                        {
                            "message_id": payload.message_id,
                            "event_type": payload.event_type,
                            "source": payload.source,
                            "data": payload.data,
                        }
                    ),
                    "attributes": payload.attributes,
                }
            ]
        },
    )
    return PublishResult(
        provider="google_pubsub",
        destination=topic_path(),
        message_ids=[str(message_id) for message_id in response.get("messageIds", [])],
    )
