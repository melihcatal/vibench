"""Consumes one message from a Google Cloud Pub/Sub managed subscription or queue.

Uses the google.cloud.pubsub_v1 SubscriberClient to pull a single message
from a managed Pub/Sub subscription, deserialize it, and return structured results.
"""

from google.cloud.pubsub_v1 import SubscriberClient

from messaging_client import get_subscriber_client, subscription_path, get_max_retries
from messaging_models import PubSubEvent, ConsumeResult


def consume_event(
    project_id: str | None = None,
    subscription_id: str | None = None,
    client: SubscriberClient | None = None,
    max_messages: int = 1,
    auto_ack: bool = False,
) -> ConsumeResult | None:
    """Consume a single message from a Google Cloud Pub/Sub subscription.

    Pulls one message from the specified subscription, deserializes it into
    a PubSubEvent, and returns a ConsumeResult with acknowledgment info.

    Args:
        project_id: GCP project ID. Uses default if not provided.
        subscription_id: Pub/Sub subscription ID. Uses default if not provided.
        client: Optional pre-configured SubscriberClient. Creates one if None.
        max_messages: Maximum messages to pull. Defaults to 1.
        auto_ack: If True, automatically acknowledge the message after pulling.

    Returns:
        ConsumeResult if a message was available, None if the subscription was empty.

    Raises:
        Exception: If the pull operation fails.
    """
    subscriber = client or get_subscriber_client()
    sub_path = subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={
            "subscription": sub_path,
            "max_messages": max_messages,
        }
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    message = received.message

    event = PubSubEvent.from_json_bytes(message.data)

    delivery_attempt = 1
    if message.delivery_attempt:
        delivery_attempt = message.delivery_attempt

    ack_id = received.ack_id

    if auto_ack:
        subscriber.acknowledge(
            request={
                "subscription": sub_path,
                "ack_ids": [ack_id],
            }
        )

    return ConsumeResult(
        event=event,
        ack_id=ack_id,
        delivery_attempt=delivery_attempt,
    )


def acknowledge_message(
    ack_id: str,
    project_id: str | None = None,
    subscription_id: str | None = None,
    client: SubscriberClient | None = None,
) -> None:
    """Acknowledge a consumed message by its acknowledgment ID.

    Args:
        ack_id: The acknowledgment ID from the consumed message.
        project_id: GCP project ID.
        subscription_id: Pub/Sub subscription ID.
        client: Optional pre-configured SubscriberClient.
    """
    subscriber = client or get_subscriber_client()
    sub_path = subscription_path(project_id, subscription_id)

    subscriber.acknowledge(
        request={
            "subscription": sub_path,
            "ack_ids": [ack_id],
        }
    )


def nack_message(
    ack_id: str,
    project_id: str | None = None,
    subscription_id: str | None = None,
    client: SubscriberClient | None = None,
) -> None:
    """Negatively acknowledge a message to make it available for redelivery.

    Args:
        ack_id: The acknowledgment ID from the consumed message.
        project_id: GCP project ID.
        subscription_id: Pub/Sub subscription ID.
        client: Optional pre-configured SubscriberClient.
    """
    subscriber = client or get_subscriber_client()
    sub_path = subscription_path(project_id, subscription_id)

    subscriber.modify_ack_deadline(
        request={
            "subscription": sub_path,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": 0,
        }
    )


if __name__ == "__main__":
    result = consume_event(auto_ack=False)
    if result:
        print(f"Consumed event: {result.event.event_type} (ID: {result.event.event_id})")
        print(f"Delivery attempt: {result.delivery_attempt}")
        print(f"Ack ID: {result.ack_id}")
    else:
        print("No messages available in subscription")
