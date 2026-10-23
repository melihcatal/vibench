from messaging_client import get_subscriber_client, get_project_id
from messaging_models import PubSubMessage


def consume_one_event(subscription_id: str, timeout: float = 5.0):
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}, timeout=timeout
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]
    ack_id = received_message.ack_id
    message_data = received_message.message.data
    message_id = received_message.message.message_id
    attributes = dict(received_message.message.attributes)

    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [ack_id]}
    )

    return PubSubMessage.from_json(message_data, message_id, attributes)
