from google.cloud import pubsub_v1
from messaging_client import get_subscriber, get_subscription_path
from messaging_models import parse_message_data

def consume_event():
    subscriber = get_subscriber()
    subscription_path = get_subscription_path()
    
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )
    
    if not response.received_messages:
        return None
    
    message = response.received_messages[0]
    data = parse_message_data(message.message.data)
    
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [message.ack_id],
        }
    )
    
    return data