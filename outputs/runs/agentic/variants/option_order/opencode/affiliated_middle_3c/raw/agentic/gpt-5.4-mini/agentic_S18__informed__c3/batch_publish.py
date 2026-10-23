import json

from messaging_client import get_publisher, topic_path
from messaging_models import (
    MessageBatchItem,
    MessageResponse,
    normalize_attributes,
    normalize_payload,
)


def batch_publish(topic: str, items: list[MessageBatchItem]) -> list[MessageResponse]:
    publisher = get_publisher()
    topic_ref = topic_path(topic)
    futures = []
    for item in items:
        futures.append(
            (
                item,
                publisher.publish(
                    topic_ref,
                    data=normalize_payload(item.payload).encode("utf-8"),
                    **normalize_attributes(item.attributes),
                ),
            )
        )
    results = []
    for item, future in futures:
        results.append(
            MessageResponse(
                message_id=future.result(),
                status="published",
                attributes={
                    "batch_item_id": item.message_id,
                    **normalize_attributes(item.attributes),
                },
            )
        )
    return results


def batch_publish_json(topic: str, messages: list[dict]) -> list[MessageResponse]:
    return batch_publish(
        topic,
        [
            MessageBatchItem(
                message_id=str(item["id"]),
                payload=json.dumps(item["payload"]),
                attributes=item.get("attributes", {}),
            )
            for item in messages
        ],
    )
