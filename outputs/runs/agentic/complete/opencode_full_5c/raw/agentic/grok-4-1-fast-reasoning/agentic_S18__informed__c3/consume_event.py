from typing import Optional
from messaging_client import get_subscriber, get_subscription_path
from messaging_models import PubSubEvent


def consume_one_event() -> Optional[PubSubEvent]:
    subscriber = get_subscriber()
    subscription_path = get_subscription_path()
    response = subscriber.pull(subscription=subscription_path, max_messages=1)
    if response.received_messages:
        message = response.received_messages[0]
        event = PubSubEvent.from_pubsub_message(message)
        subscriber.acknowledge(subscription=subscription_path, ack_ids=[message.ack_id])
        return event
    return None
