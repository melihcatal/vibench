from messaging_client import get_subscriber_client, get_subscription_name
from messaging_models import parse_pubsub_message

def consume_single_event(subscription_id: str, timeout: float = 5.0):
    """Consumes a single message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        A dictionary representing the parsed message payload, or None if no message is received.
    """
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_name(subscription_id)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        timeout=timeout
    )

    if not response.received_messages:
        return None

    for received_message in response.received_messages:
        message_data = parse_pubsub_message(received_message.message.data)
        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [received_message.ack_id],
            }
        )
        return message_data
    return None
