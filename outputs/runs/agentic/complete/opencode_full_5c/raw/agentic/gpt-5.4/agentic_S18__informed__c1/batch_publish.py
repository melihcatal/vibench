from __future__ import annotations

from typing import Any

from messaging_client import publish_batch
from messaging_models import BatchPublishItem, normalize_payload


def batch_publish(topic_arn: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
    items = []
    for message in messages:
        items.append(
            BatchPublishItem(
                payload=normalize_payload(message.get("payload", {})),
                subject=message.get("subject"),
                attributes={
                    str(k): str(v) for k, v in message.get("attributes", {}).items()
                },
                message_id=str(message.get("id") or message.get("message_id") or ""),
            )
        )
    normalized_items = [
        item
        if item.message_id
        else BatchPublishItem(
            payload=item.payload, subject=item.subject, attributes=item.attributes
        )
        for item in items
    ]
    response = publish_batch(topic_arn, normalized_items)
    return {
        "provider": "aws_sns",
        "topic_arn": topic_arn,
        "successful": response.get("Successful", []),
        "failed": response.get("Failed", []),
    }
