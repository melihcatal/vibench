from google.cloud import pubsub_v1
import os
import json
from typing import Optional, Dict, Any
from messaging_models import Event

subscriber = pubsub_v1.SubscriberClient()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
subscription_id = os.getenv("GOOGLE_PUBSUB_SUBSCRIPTION_ID")


def consume_event() -> Optional[Dict[str, Any]]:
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )
    if not response.received_messages:
        return None

    message = response.received_messages[0]
    event_data = json.loads(message.message.data.decode("utf-8"))
    event = Event(**event_data).dict()

    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [message.ack_id],
        }
    )

    return event
