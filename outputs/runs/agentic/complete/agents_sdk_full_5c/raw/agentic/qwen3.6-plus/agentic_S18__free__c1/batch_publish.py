"""batch_publish.py - Publishes a batch of messages with IDs or attributes to Google Cloud Pub/Sub."""

import json
import logging
import uuid
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError
from messaging_client import get_pubsub_publisher_client, PUBSUB_TOPIC_ID, PUBSUB_PROJECT_ID
from messaging_models import PubSubBatchPublishRequest, PubSubBatchPublishResponse, PubSubMessageEntry

logger = logging.getLogger(__name__)


def batch_publish(messages: list[PubSubMessageEntry]) -> PubSubBatchPublishResponse:
    """Publish a batch of messages with IDs and attributes to Google Cloud Pub/Sub.

    Args:
        messages: List of PubSubMessageEntry objects containing payload and attributes.

    Returns:
        PubSubBatchPublishResponse with results for each message.
    """
    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID)

    batch_request = PubSubBatchPublishRequest(
        topic_path=topic_path,
        messages=messages,
    )

    results = []
    futures = []

    for entry in batch_request.messages:
        message_id = entry.message_id or str(uuid.uuid4())
        attributes = {
            "message_id": message_id,
            "content_type": "application/json",
        }
        attributes.update(entry.attributes or {})

        payload = json.dumps(entry.payload).encode("utf-8")

        try:
            future = publisher.publish(
                batch_request.topic_path,
                payload,
                **attributes,
            )
            futures.append((message_id, future, entry))
        except GoogleAPIError as exc:
            logger.error("Failed to queue message %s: %s", message_id, exc)
            results.append(
                {"message_id": message_id, "status": "failed", "error": str(exc)}
            )

    for message_id, future, entry in futures:
        try:
            published_id = future.result(timeout=30)
            logger.info("Batch published %s -> %s", message_id, published_id)
            results.append(
                {
                    "message_id": message_id,
                    "published_id": published_id,
                    "status": "published",
                }
            )
        except GoogleAPIError as exc:
            logger.error("Failed to confirm publish for %s: %s", message_id, exc)
            results.append(
                {"message_id": message_id, "status": "failed", "error": str(exc)}
            )

    published_count = sum(1 for r in results if r["status"] == "published")
    failed_count = sum(1 for r in results if r["status"] == "failed")

    logger.info(
        "Batch publish complete: %d published, %d failed",
        published_count,
        failed_count,
    )

    return PubSubBatchPublishResponse(
        topic_name=batch_request.topic_path,
        total=len(messages),
        published_count=published_count,
        failed_count=failed_count,
        results=results,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    batch_messages = [
        PubSubMessageEntry(
            message_id="batch_msg_001",
            payload={"event_type": "order_created", "order_id": "ORD-1001"},
            attributes={"priority": "high"},
        ),
        PubSubMessageEntry(
            message_id="batch_msg_002",
            payload={"event_type": "inventory_update", "sku": "SKU-2024"},
            attributes={"priority": "normal"},
        ),
        PubSubMessageEntry(
            message_id="batch_msg_003",
            payload={"event_type": "shipment_dispatched", "tracking": "TRK-9988"},
            attributes={"priority": "low"},
        ),
    ]
    result = batch_publish(batch_messages)
    print(f"Batch publish result: {result}")
