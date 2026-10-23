import json
from concurrent.futures import TimeoutError

from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import parse_message_payload

def consume_event(config=None):
    config = config or {}
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscriber, config["subscription_id"])

    # The subscriber pulls messages synchronously. This is suitable for consuming a single message.
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1})

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]
    message_data = parse_message_payload(received_message.message)

    # Acknowledge the message
    ack_ids = [received_message.ack_id]
    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})

    subscriber.close()
    return message_data
