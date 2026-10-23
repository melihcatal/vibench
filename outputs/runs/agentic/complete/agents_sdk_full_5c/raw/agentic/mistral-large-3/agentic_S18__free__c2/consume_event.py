import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_subscriber
from messaging_models import EventResponse

subscriber = get_pubsub_subscriber()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
SUBSCRIPTION_NAME = os.getenv("PUBSUB_SUBSCRIPTION_NAME", "orders-v1-sub")

def consume_event() -> EventResponse:
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
    
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )
    
    if not response.received_messages:
        return None
    
    message = response.received_messages[0]
    event_response = EventResponse(
        message_id=message.message.message_id,
        payload=json.loads(message.message.data.decode("utf-8")),
        attributes=message.message.attributes,
        ack_id=message.ack_id
    )
    return event_response