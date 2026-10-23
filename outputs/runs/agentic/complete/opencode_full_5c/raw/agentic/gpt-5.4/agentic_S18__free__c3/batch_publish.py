from __future__ import annotations

from typing import Any, Dict, Iterable

from messaging_client import pubsub_post, topic_path
from messaging_models import MessagePayload, PublishResult, encode_message_data


def batch_publish(events: Iterable[Dict[str, Any]]) -> PublishResult:
    messages = []
    for event in events:
        payload = MessagePayload.from_dict(event)
        attributes = {
            **payload.attributes,
            "message_id": payload.message_id,
            "event_type": payload.event_type,
        }
        messages.append(
            {
                "data": encode_message_data(
                    {
                        "message_id": payload.message_id,
                        "event_type": payload.event_type,
                        "source": payload.source,
                        "data": payload.data,
                    }
                ),
                "attributes": attributes,
                "orderingKey": payload.message_id,
            }
        )
    response = pubsub_post(f"{topic_path()}:publish", {"messages": messages})
    return PublishResult(
        provider="google_pubsub",
        destination=topic_path(),
        message_ids=[str(message_id) for message_id in response.get("messageIds", [])],
    )
