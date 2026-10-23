import os
import json
from typing import Dict, Any
from datetime import datetime
from messaging_client import PubSubClient
from messaging_models import create_error_payload


def send_to_dead_letter(
    original_topic: str,
    original_message: Dict[str, Any],
    error_type: str,
    error_details: str,
    max_retries: int = 3,
) -> str:
    client = PubSubClient()

    dead_letter_topic_name = client.create_dead_letter_topic_name(original_topic)
    dead_letter_topic_path = client.get_topic_path(dead_letter_topic_name)

    error_payload = create_error_payload(error_type, original_message, error_details)

    dead_letter_message = {
        "original_topic": original_topic,
        "original_message": original_message,
        "error_type": error_type,
        "error_details": error_details,
        "timestamp": datetime.utcnow().isoformat(),
        "retry_count": 0,
        "max_retries": max_retries,
    }

    message_data = json.dumps(dead_letter_message).encode("utf-8")

    attributes = {
        "error_type": error_type,
        "original_topic": original_topic,
        "retry_count": "0",
    }

    future = client.publisher_client.publish(
        dead_letter_topic_path, data=message_data, **attributes
    )

    message_id = future.result()

    return message_id


def process_failed_message(
    subscription_id: str, message_data: Dict[str, Any], error: Exception
) -> str:
    client = PubSubClient()

    original_topic = message_data.get("attributes", {}).get("original_topic", "unknown")

    error_type = type(error).__name__
    error_details = str(error)

    dead_letter_id = send_to_dead_letter(
        original_topic=original_topic,
        original_message=message_data,
        error_type=error_type,
        error_details=error_details,
    )

    subscription_path = client.get_subscription_path(subscription_id)

    if "ack_id" in message_data:
        client.subscriber_client.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [message_data["ack_id"]],
            }
        )

    return dead_letter_id


def create_dead_letter_subscription(
    original_topic: str, subscription_suffix: str = "-dlq"
) -> str:
    client = PubSubClient()

    dead_letter_topic_name = client.create_dead_letter_topic_name(original_topic)
    dead_letter_topic_path = client.get_topic_path(dead_letter_topic_name)

    subscription_name = f"{dead_letter_topic_name}{subscription_suffix}"
    subscription_path = client.get_subscription_path(subscription_name)

    try:
        client.subscriber_client.create_subscription(
            request={
                "name": subscription_path,
                "topic": dead_letter_topic_path,
            }
        )
    except Exception:
        pass

    return subscription_name


if __name__ == "__main__":
    sample_failed_message = {
        "data": {
            "event_type": "user_registered",
            "data": {"user_id": "test_123"},
            "timestamp": "2024-01-15T10:30:00Z",
            "source": "auth_service",
        },
        "attributes": {"original_topic": "user-events", "priority": "normal"},
        "message_id": "test_message_123",
        "ack_id": "test_ack_123",
    }

    try:
        dead_letter_id = process_failed_message(
            "user-events-subscription",
            sample_failed_message,
            ValueError("Invalid user data format"),
        )
        print(f"Sent to dead letter with ID: {dead_letter_id}")

        dl_subscription = create_dead_letter_subscription("user-events")
        print(f"Created dead letter subscription: {dl_subscription}")
    except Exception as e:
        print(f"Failed to process dead letter: {e}")
