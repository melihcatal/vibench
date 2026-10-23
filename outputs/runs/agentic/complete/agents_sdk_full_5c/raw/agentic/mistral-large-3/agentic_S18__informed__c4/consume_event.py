import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_subscriber
from messaging_models import EventMessage

subscriber = get_pubsub_subscriber()

def consume_event(subscription_name: str) -> EventMessage:
    subscription_path = subscriber.subscription_path(os.getenv("GOOGLE_CLOUD_PROJECT"), subscription_name)
    response = subscriber.pull(subscription_path, max_messages=1, return_immediately=True)
    
    if not response.received_messages:
        return None
    
    message = response.received_messages[0]
    event = EventMessage(
        data=message.message.data.decode("utf-8"),
        attributes=message.message.attributes,
        message_id=message.message.message_id
    )
    
    subscriber.acknowledge(subscription_path, [message.ack_id])
    return event