import json
from messaging_client import get_subscriber_client, subscription_path


def consume_one_message():
    """Consumes and acknowledges one message from the configured subscription."""
    subscriber = get_subscriber_client()

    response = subscriber.pull(
        subscription=subscription_path, max_messages=1, return_immediately=True
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]
    message_data = json.loads(received_message.message.data.decode("utf-8"))

    subscriber.acknowledge(
        subscription=subscription_path, ack_ids=[received_message.ack_id]
    )

    return message_data
