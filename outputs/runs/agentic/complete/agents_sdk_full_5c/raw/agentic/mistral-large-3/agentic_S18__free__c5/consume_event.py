import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

subscriber = get_pubsub_client(client_type="subscriber")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
SUBSCRIPTION_NAME = os.getenv("PUBSUB_SUBSCRIPTION_NAME", "orders-subscription")

def consume_event() -> EventMessage:
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
    
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": False,
        }
    )
    
    if not response.received_messages:
        return None
    
    message = response.received_messages[0]
    event_data = json.loads(message.message.data.decode("utf-8"))
    event = EventMessage(**event_data)
    
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [message.ack_id],
        }
    )
    
    return event