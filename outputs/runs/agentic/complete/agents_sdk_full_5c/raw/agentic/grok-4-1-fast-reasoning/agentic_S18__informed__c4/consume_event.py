import json
from google.cloud import pubsub_v1
from messaging_client import get_subscriber, get_subscription_path
from messaging_models import PubSubMessage

def consume_event() -> list[PubSubMessage]:
    subscriber = get_subscriber()
    subscription_path = get_subscription_path()
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )
    messages = []
    ack_ids = []
    for received_message in response.received_messages:
        data = json.loads(received_message.message.data.decode("utf-8"))
        msg = PubSubMessage(
            id=received_message.message.message_id,
            data=data,
            attributes=dict(received_message.message.attributes)
        )
        messages.append(msg)
        ack_ids.append(received_message.ack_id)
    if ack_ids:
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )
    return messages