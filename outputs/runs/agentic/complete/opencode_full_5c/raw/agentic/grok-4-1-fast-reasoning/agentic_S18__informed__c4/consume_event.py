from google.cloud import pubsub_v1
from typing import Optional
from messaging_client import PubSubClient
from messaging_models import PubSubMessage, decode_message_data


def consume_event() -> Optional[PubSubMessage]:
    client = PubSubClient()
    response = client.subscriber.pull(
        subscription=client.subscription_path, max_messages=1, return_immediately=True
    )
    if not response.received_messages:
        return None
    received_message = response.received_messages[0]
    data = decode_message_data(received_message.message.data)
    attributes = dict(received_message.message.attributes)
    pubsub_msg = PubSubMessage(
        id=received_message.message.message_id, data=data, attributes=attributes
    )
    client.subscriber.acknowledge(
        subscription=client.subscription_path, ack_ids=[received_message.ack_id]
    )
    return pubsub_msg
