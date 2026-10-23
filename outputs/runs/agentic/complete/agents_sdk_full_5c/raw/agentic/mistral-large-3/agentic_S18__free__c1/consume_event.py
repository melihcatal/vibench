import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_subscriber
from messaging_models import EventResponse

subscriber = get_pubsub_subscriber()
subscription_path = subscriber.subscription_path(
    os.getenv("GOOGLE_CLOUD_PROJECT"), 
    os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
)

def consume_event() -> EventResponse:
    response = subscriber.pull(
        subscription=subscription_path,
        max_messages=1,
        return_immediately=True
    )
    if not response.received_messages:
        return None
    
    message = response.received_messages[0]
    event_data = json.loads(message.message.data.decode("utf-8"))
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[message.ack_id])
    
    return EventResponse(**event_data, message_id=message.message.message_id)