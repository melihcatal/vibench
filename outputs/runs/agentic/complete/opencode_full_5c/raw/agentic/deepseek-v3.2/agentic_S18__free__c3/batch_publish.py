import os
import json
import uuid
from google.cloud import pubsub_v1


def publish_batch(messages, topic_id=None, batch_settings=None):
    """Publishes a batch of messages with IDs or attributes."""
    if topic_id is None:
        topic_id = os.environ.get(
            "PUBSUB_TOPIC_ID", "projects/my-project/topics/my-topic"
        )

    if batch_settings is None:
        batch_settings = {
            "max_messages": 100,
            "max_bytes": 10 * 1024 * 1024,  # 10 MB
            "max_latency": 1.0,  # 1 second
        }

    publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=False,
    )

    batch_settings_obj = pubsub_v1.types.BatchSettings(
        max_messages=batch_settings["max_messages"],
        max_bytes=batch_settings["max_bytes"],
        max_latency=batch_settings["max_latency"],
    )

    publisher = pubsub_v1.PublisherClient(
        publisher_options=publisher_options, batch_settings=batch_settings_obj
    )

    futures = []
    message_ids = []

    for i, message in enumerate(messages):
        # Generate message ID if not provided
        message_id = message.get("id", str(uuid.uuid4()))

        # Prepare data
        if isinstance(message.get("data"), dict):
            data = json.dumps(message["data"]).encode("utf-8")
        else:
            data = str(message.get("data", "")).encode("utf-8")

        # Prepare attributes
        attributes = message.get("attributes", {})
        attributes["batch_index"] = str(i)
        attributes["message_id"] = message_id

        # Publish with callback
        future = publisher.publish(topic_id, data, **attributes)
        futures.append(future)

    # Wait for all publishes to complete
    for future in futures:
        try:
            pubsub_message_id = future.result()
            message_ids.append(pubsub_message_id)
        except Exception as e:
            print(f"Failed to publish message: {e}")

    return {
        "topic": topic_id,
        "published_count": len(message_ids),
        "message_ids": message_ids,
        "total_messages": len(messages),
    }


if __name__ == "__main__":
    # Example batch of messages
    batch_messages = [
        {
            "id": "msg_001",
            "data": {"event": "user_login", "user_id": "user_001"},
            "attributes": {"priority": "high", "source": "web"},
        },
        {
            "id": "msg_002",
            "data": {"event": "order_placed", "order_id": "order_123"},
            "attributes": {"priority": "medium", "source": "mobile"},
        },
        {
            "id": "msg_003",
            "data": {"event": "page_view", "page": "/home"},
            "attributes": {"priority": "low", "source": "web"},
        },
    ]

    result = publish_batch(batch_messages)
    print(
        f"Published {result['published_count']} of {result['total_messages']} messages"
    )
    print(f"Message IDs: {result['message_ids']}")
