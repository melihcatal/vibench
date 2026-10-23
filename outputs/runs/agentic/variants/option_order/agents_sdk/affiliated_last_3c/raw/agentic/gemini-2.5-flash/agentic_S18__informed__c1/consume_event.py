import os
import json
from typing import Optional, Dict, Any
from google.cloud.pubsub_v1 import SubscriberClient
from messaging_client import get_pubsub_subscriber_client
from messaging_models import ConsumeResponse

def consume_event(subscription_id: str, timeout: Optional[float] = 5.0) -> Optional[ConsumeResponse]:
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    subscriber = get_pubsub_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True})

    if response.received_messages:
        received_message = response.received_messages[0]
        message = received_message.message

        payload = json.loads(message.data.decode("utf-8"))
        attributes = dict(message.attributes)

        return ConsumeResponse(
            message_id=message.message_id,
            payload=payload,
            attributes=attributes,
            ack_id=received_message.ack_id
        )
    return None

def acknowledge_message(ack_id: str, subscription_id: str):
    """Acknowledges a message in Google Cloud Pub/Sub."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    
    subscriber = get_pubsub_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    
    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [ack_id]})

