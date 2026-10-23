import os
import json
from typing import Dict, Any
from messaging_client import PubSubClient
from messaging_models import MessagePayload


def publish_event(
    topic_id: str, event_data: Dict[str, Any], attributes: Dict[str, str] = None
) -> str:
    client = PubSubClient()

    payload = MessagePayload(
        event_type=event_data.get("event_type", "custom_event"),
        data=event_data.get("data", {}),
        timestamp=event_data.get("timestamp"),
        source=event_data.get("source", "publish_event"),
        version=event_data.get("version", "1.0"),
    )

    if not payload.timestamp:
        from datetime import datetime

        payload.timestamp = datetime.utcnow().isoformat()

    message_data = payload.to_json().encode("utf-8")

    topic_path = client.get_topic_path(topic_id)

    future = client.publisher_client.publish(
        topic_path, data=message_data, **attributes if attributes else {}
    )

    message_id = future.result()

    return message_id


if __name__ == "__main__":
    sample_event = {
        "event_type": "user_registered",
        "data": {
            "user_id": "user_12345",
            "email": "user@example.com",
            "registration_date": "2024-01-15T10:30:00Z",
        },
        "timestamp": "2024-01-15T10:30:00Z",
        "source": "auth_service",
        "version": "1.0",
    }

    attributes = {"event_category": "authentication", "priority": "normal"}

    try:
        message_id = publish_event("user-events", sample_event, attributes)
        print(f"Published event with message ID: {message_id}")
    except Exception as e:
        print(f"Failed to publish event: {e}")
