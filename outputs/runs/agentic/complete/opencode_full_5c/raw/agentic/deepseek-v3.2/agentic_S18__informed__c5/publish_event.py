import os
import json
from messaging_client import MessagingClient
from messaging_models import create_event_message


def publish_event(
    topic_id, event_type, payload, source, correlation_id=None, attributes=None
):
    client = MessagingClient()

    event_message = create_event_message(
        event_type=event_type,
        payload=payload,
        source=source,
        correlation_id=correlation_id,
    )

    topic_path = client.get_topic_path(topic_id)

    message_data = event_message.to_json()

    publish_attributes = attributes or {}
    if correlation_id:
        publish_attributes["correlation_id"] = correlation_id
    publish_attributes["event_type"] = event_type
    publish_attributes["source"] = source

    try:
        message_id = client.publish_message(
            topic_path, message_data, publish_attributes
        )
        print(f"Published event to {topic_id} with message ID: {message_id}")
        return message_id
    except Exception as e:
        print(f"Failed to publish event to Google Cloud Pub/Sub topic {topic_id}: {e}")
        raise


if __name__ == "__main__":
    sample_payload = {
        "user_id": "user_123",
        "action": "login",
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0",
    }

    try:
        message_id = publish_event(
            topic_id="user-events",
            event_type="user_login",
            payload=sample_payload,
            source="auth_service",
            correlation_id="corr_001",
        )
        print(f"Successfully published message with ID: {message_id}")
    except Exception as e:
        print(f"Error: {e}")
