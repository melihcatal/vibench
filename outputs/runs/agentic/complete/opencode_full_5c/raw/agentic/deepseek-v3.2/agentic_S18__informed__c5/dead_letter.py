import os
import json
from datetime import datetime
from messaging_client import MessagingClient
from messaging_models import EventMessage


def send_to_dead_letter(
    dead_letter_topic_id,
    original_message,
    failure_reason,
    original_subscription=None,
    delivery_attempts=None,
):
    client = MessagingClient()

    dead_letter_topic_path = client.get_dead_letter_topic_path(dead_letter_topic_id)

    dead_letter_payload = {
        "original_message": original_message,
        "failure_reason": failure_reason,
        "failed_at": datetime.utcnow().isoformat(),
        "original_subscription": original_subscription,
        "delivery_attempts": delivery_attempts,
    }

    dead_letter_data = json.dumps(dead_letter_payload).encode("utf-8")

    attributes = {
        "failure_reason": failure_reason[:100],
        "failed_at": dead_letter_payload["failed_at"],
    }

    if original_subscription:
        attributes["original_subscription"] = original_subscription

    if delivery_attempts:
        attributes["delivery_attempts"] = str(delivery_attempts)

    try:
        message_id = client.publish_message(
            dead_letter_topic_path, dead_letter_data, attributes
        )
        print(
            f"Sent failed message to Google Cloud Pub/Sub dead letter topic {dead_letter_topic_id} with ID: {message_id}"
        )
        return message_id
    except Exception as e:
        print(
            f"Failed to send to Google Cloud Pub/Sub dead letter topic {dead_letter_topic_id}: {e}"
        )
        raise


def process_failed_message(subscription_id, message_data, attributes, failure_reason):
    client = MessagingClient()

    dead_letter_topic_id = f"{subscription_id}-dead-letter"

    try:
        event_message = EventMessage.from_json(message_data)

        dead_letter_message_id = send_to_dead_letter(
            dead_letter_topic_id=dead_letter_topic_id,
            original_message={
                "event_type": event_message.event_type,
                "payload": event_message.payload,
                "source": event_message.source,
                "correlation_id": event_message.correlation_id,
                "timestamp": event_message.timestamp,
            },
            failure_reason=failure_reason,
            original_subscription=subscription_id,
            delivery_attempts=attributes.get("delivery_attempt_count", 1)
            if attributes
            else 1,
        )

        subscription_path = client.get_subscription_path(subscription_id)

        dead_letter_topic_path = client.get_dead_letter_topic_path(dead_letter_topic_id)
        dead_letter_config = client.create_dead_letter_config(dead_letter_topic_path)

        print(f"Configured dead letter policy for subscription {subscription_id}")
        print(f"Dead letter topic: {dead_letter_topic_id}")
        print(f"Max delivery attempts: {dead_letter_config.max_delivery_attempts}")

        return {
            "dead_letter_message_id": dead_letter_message_id,
            "dead_letter_topic": dead_letter_topic_id,
            "failure_reason": failure_reason,
            "processed_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        print(f"Failed to process dead letter for subscription {subscription_id}: {e}")
        raise


if __name__ == "__main__":
    sample_message_data = json.dumps(
        {
            "event_type": "user_login",
            "payload": {"user_id": "user_123", "action": "login"},
            "source": "auth_service",
            "timestamp": datetime.utcnow().isoformat(),
            "correlation_id": "corr_001",
        }
    ).encode("utf-8")

    sample_attributes = {"event_type": "user_login", "delivery_attempt_count": "3"}

    try:
        result = process_failed_message(
            subscription_id="user-events-subscription",
            message_data=sample_message_data,
            attributes=sample_attributes,
            failure_reason="Payload validation failed: missing required field 'session_id'",
        )
        print(f"Dead letter processing result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
