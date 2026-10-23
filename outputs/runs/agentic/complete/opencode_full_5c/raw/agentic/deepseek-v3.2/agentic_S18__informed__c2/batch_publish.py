import os
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from messaging_client import PubSubClient
from messaging_models import MessagePayload, BatchMessage


def publish_batch(
    topic_id: str,
    messages: List[Dict[str, Any]],
    batch_attributes: Optional[Dict[str, str]] = None,
) -> List[str]:
    client = PubSubClient()

    topic_path = client.get_topic_path(topic_id)

    batch_messages = []
    for msg_data in messages:
        msg_id = str(uuid.uuid4())

        payload = MessagePayload(
            event_type=msg_data.get("event_type", "batch_event"),
            data=msg_data.get("data", {}),
            timestamp=msg_data.get("timestamp", datetime.utcnow().isoformat()),
            source=msg_data.get("source", "batch_publisher"),
            version=msg_data.get("version", "1.0"),
        )

        attributes = msg_data.get("attributes", {})
        attributes["batch_message_id"] = msg_id

        if batch_attributes:
            attributes.update(batch_attributes)

        batch_message = BatchMessage(id=msg_id, payload=payload, attributes=attributes)

        batch_messages.append(batch_message)

    futures = []
    for batch_msg in batch_messages:
        publish_data = batch_msg.to_publish_format()

        future = client.publisher_client.publish(
            topic_path, data=publish_data["data"], **publish_data["attributes"]
        )

        futures.append((batch_msg.id, future))

    message_ids = []
    for msg_id, future in futures:
        try:
            pubsub_message_id = future.result()
            message_ids.append({"batch_id": msg_id, "pubsub_id": pubsub_message_id})
        except Exception as e:
            print(f"Failed to publish message {msg_id}: {e}")
            message_ids.append({"batch_id": msg_id, "error": str(e)})

    return message_ids


def create_batch_messages(
    event_type: str, items: List[Dict[str, Any]], source: str = "batch_processor"
) -> List[Dict[str, Any]]:
    messages = []

    for i, item in enumerate(items):
        message = {
            "event_type": event_type,
            "data": item,
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "version": "1.0",
            "attributes": {"batch_index": str(i), "total_items": str(len(items))},
        }
        messages.append(message)

    return messages


if __name__ == "__main__":
    sample_items = [
        {"user_id": "user_1", "action": "login", "timestamp": "2024-01-15T10:30:00Z"},
        {"user_id": "user_2", "action": "logout", "timestamp": "2024-01-15T10:31:00Z"},
        {
            "user_id": "user_3",
            "action": "purchase",
            "timestamp": "2024-01-15T10:32:00Z",
            "amount": 49.99,
        },
    ]

    batch_messages = create_batch_messages(
        "user_activity", sample_items, "activity_tracker"
    )

    batch_attrs = {
        "batch_id": str(uuid.uuid4()),
        "processor": "batch_publish.py",
        "priority": "normal",
    }

    try:
        results = publish_batch("user-activities", batch_messages, batch_attrs)

        success_count = sum(1 for r in results if "pubsub_id" in r)
        error_count = sum(1 for r in results if "error" in r)

        print(
            f"Batch publish completed: {success_count} successful, {error_count} failed"
        )

        for result in results:
            if "pubsub_id" in result:
                print(f"  Published: {result['batch_id']} -> {result['pubsub_id']}")
            else:
                print(f"  Failed: {result['batch_id']} - {result['error']}")

    except Exception as e:
        print(f"Failed to publish batch: {e}")
