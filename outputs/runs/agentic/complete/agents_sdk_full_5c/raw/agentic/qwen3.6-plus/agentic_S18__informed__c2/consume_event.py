"""
Consume one message from a Google Cloud Pub/Sub managed subscription.

Uses the google-cloud-pubsub SDK to pull a single message from a subscription.
Requires GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
"""

import os
import json
from typing import Optional

from google.cloud import pubsub_v1

from messaging_models import ConsumedMessage, MessagingEvent
from messaging_client import PubSubClientHelper


def consume_event(
    subscription_id: str,
    project_id: Optional[str] = None,
    auto_acknowledge: bool = True,
) -> Optional[ConsumedMessage]:
    """
    Consume one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The Pub/Sub subscription ID to pull from.
        project_id: Optional GCP project ID (falls back to GCP_PROJECT_ID env var).
        auto_acknowledge: Whether to automatically acknowledge the message.

    Returns:
        ConsumedMessage if available, None if no messages.
    """
    helper = PubSubClientHelper(project_id=project_id)

    try:
        received_messages = helper.pull_message(
            subscription_id=subscription_id,
            max_messages=1,
        )

        if not received_messages:
            return None

        received = received_messages[0]
        message = received.message

        consumed = ConsumedMessage(
            message_id=message.message_id,
            data=message.data.decode("utf-8"),
            attributes=dict(message.attributes),
            raw=message,
        )

        if auto_acknowledge and received.ack_id:
            helper.acknowledge_message(
                subscription_id=subscription_id,
                ack_id=received.ack_id,
            )
            consumed.acknowledged = True

        return consumed

    except Exception as e:
        print(f"Error consuming message: {e}")
        return None
    finally:
        helper.close()


def consume_and_parse_event(
    subscription_id: str,
    project_id: Optional[str] = None,
    auto_acknowledge: bool = True,
) -> Optional[MessagingEvent]:
    """
    Consume one message and parse it into a MessagingEvent.

    Args:
        subscription_id: The Pub/Sub subscription ID.
        project_id: Optional GCP project ID.
        auto_acknowledge: Whether to auto-acknowledge.

    Returns:
        Parsed MessagingEvent or None.
    """
    consumed = consume_event(
        subscription_id=subscription_id,
        project_id=project_id,
        auto_acknowledge=auto_acknowledge,
    )

    if consumed is None:
        return None

    return consumed.get_payload()


if __name__ == "__main__":
    subscription = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
    result = consume_event(subscription)
    if result:
        print(json.dumps({
            "message_id": result.message_id,
            "data": result.data,
            "attributes": result.attributes,
            "acknowledged": result.acknowledged,
        }, indent=2))
    else:
        print("No messages available")
