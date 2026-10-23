import os
from google.cloud import pubsub_v1
from messaging_client import get_messaging_config
from messaging_models import normalize_message, MessageEvent

def consume_event(subscription: str = None, max_messages: int = 1) -&gt; MessageEvent:
    config = get_messaging_config()
    project_id = config['project_id']
    subscription_name = subscription or config['subscription']
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    
    response = subscriber.pull(
        request={
            'subscription': subscription_path,
            'max_messages': max_messages,
        },
        timeout=10.0,
    )
    if not response.received_messages:
        return None
    
    received_message = response.received_messages[0]  # one
    subscriber.acknowledge(
        request={
            'subscription': subscription_path,
            'ack_ids': [received_message.ack_id],
        },
    )
    return normalize_message(received_message.message)