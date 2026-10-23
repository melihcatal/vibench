from typing import Dict, Any, Optional
from google.cloud import pubsub_v1
from messaging_client import subscription_path, SUBSCRIPTION_ID
from messaging_models import deserialize_event

def consume_event(max_messages: int = 1, timeout: float = 10.0) -> Optional[Dict[str, Any]]:
    subscriber = pubsub_v1.SubscriberClient()
    subscription = subscription_path(SUBSCRIPTION_ID)
    response = subscriber.pull(
        request={
            "subscription": subscription,
            "max_messages": max_messages,
            "timeout": timeout,
        }
    )
    if response.received_messages:
        message = response.received_messages[0]
        ack_request = {
            "subscription": subscription,
            "ack_ids": [message.ack_id],
        }
        subscriber.acknowledge(request=ack_request)
        return deserialize_event(message.message.data)
    return None
