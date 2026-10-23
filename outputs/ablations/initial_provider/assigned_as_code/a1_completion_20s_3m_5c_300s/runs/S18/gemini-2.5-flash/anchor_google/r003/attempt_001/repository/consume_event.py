from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_project_id, get_subscription_path
from messaging_models import parse_message_payload, PubsubMessage


def consume_event(config=None):
    config = config or {}
    project_id = config.get("project_id", get_project_id())
    subscription_id = config["subscription_id"]
    
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True})

    if response.received_messages:
        received_message = response.received_messages[0]
        message = received_message.message
        
        payload = parse_message_payload(message.data)
        attributes = dict(message.attributes)
        message_id = message.message_id
        
        # Acknowledge the message
        ack_ids = [received_message.ack_id]
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})
        
        return PubsubMessage(data=payload, attributes=attributes, message_id=message_id).to_dict()
    
    return None
