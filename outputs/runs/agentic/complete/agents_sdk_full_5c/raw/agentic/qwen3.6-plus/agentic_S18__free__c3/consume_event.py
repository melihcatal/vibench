"""Consume one message from a Google Cloud Pub/Sub managed subscription.

Uses Google Cloud Pub/Sub as the concrete external provider.
"""

from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import get_subscriber_client, get_subscription_path, decode_message
from messaging_models import EventMessage, MessageResponse


def consume_event(
    subscription_path: Optional[str] = None,
    project: Optional[str] = None,
    subscription_name: Optional[str] = None,
    timeout: float = 5.0,
) -> Optional[EventMessage]:
    """Pull and return a single EventMessage from Google Cloud Pub/Sub.

    Args:
        subscription_path: Optional fully-qualified subscription path.
        project: Optional GCP project ID override.
        subscription_name: Optional subscription name override.
        timeout: Max seconds to wait for a message.

    Returns:
        EventMessage if one is available, otherwise None.
    """
    try:
        subscriber = get_subscriber_client()
        sub_path = subscription_path or get_subscription_path(project=project, subscription_name=subscription_name)

        response = subscriber.pull(
            request={"subscription": sub_path, "max_messages": 1},
            timeout=timeout,
        )

        if not response.received_messages:
            return None

        received = response.received_messages[0]
        message_data = decode_message(received.message.data)

        event = EventMessage.from_dict(message_data)

        # Acknowledge the message
        ack_id = received.ack_id
        subscriber.acknowledge(request={"subscription": sub_path, "ack_ids": [ack_id]})

        return event
    except Exception:
        return None


def consume_with_response(
    subscription_path: Optional[str] = None,
    project: Optional[str] = None,
    subscription_name: Optional[str] = None,
    timeout: float = 5.0,
) -> MessageResponse:
    """Pull and return a MessageResponse wrapping the consumed event.

    Args:
        subscription_path: Optional fully-qualified subscription path.
        project: Optional GCP project ID override.
        subscription_name: Optional subscription name override.
        timeout: Max seconds to wait for a message.

    Returns:
        MessageResponse with the event details or an error.
    """
    event = consume_event(
        subscription_path=subscription_path,
        project=project,
        subscription_name=subscription_name,
        timeout=timeout,
    )

    if event is None:
        return MessageResponse(
            success=False,
            error="No messages available in the subscription",
        )

    return MessageResponse(
        success=True,
        event_id=event.event_id,
        details={"event_type": event.event_type, "source": event.source, "payload": event.payload},
    )
