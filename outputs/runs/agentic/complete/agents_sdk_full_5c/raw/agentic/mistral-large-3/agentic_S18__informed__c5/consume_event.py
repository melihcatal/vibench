from google.cloud import pubsub_v1
import os
from messaging_models import Event
from messaging_client import get_subscriber_client

def consume_event(subscription_id: str) -> Event:
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(os.getenv("GOOGLE_CLOUD_PROJECT"), subscription_id)
    
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1, "return_immediately": False}
    )
    
    if not response.received_messages:
        return None
    
    message = response.received_messages[0]
    event = Event.model_validate_json(message.message.data)
    event.message_id = message.message.message_id
    event.attributes = dict(message.message.attributes)
    
    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [message.ack_id]})
    return event