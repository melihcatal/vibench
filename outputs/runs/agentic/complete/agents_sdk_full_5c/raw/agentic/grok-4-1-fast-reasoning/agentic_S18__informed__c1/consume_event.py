import json
from typing import Dict, Any, Optional
from google.cloud import pubsub_v1
from messaging_client import PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION_ID

def consume_event() -> Optional[Dict[str, Any]]:
    """
    Consumes one message from the managed Pub/Sub subscription.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION_ID)
    
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )
    
    if not response.received_messages:
        return None
    
    message = response.received_messages[0]
    
    data = json.loads(message.message.data.decode("utf-8"))
    ack_id = message.ack_id
    
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [ack_id]}
    )
    
    data["message_id"] = message.message.message_id
    return data