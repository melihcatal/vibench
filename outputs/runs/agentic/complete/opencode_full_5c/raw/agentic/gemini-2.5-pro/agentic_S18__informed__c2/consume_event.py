from concurrent.futures import TimeoutError
from messaging_client import get_subscriber_client, get_subscription_path


def consume_event(subscription_id: str, timeout: float = 5.0):
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        retry=None,
        timeout=timeout,
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]

    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [received_message.ack_id],
        }
    )

    return received_message.message
