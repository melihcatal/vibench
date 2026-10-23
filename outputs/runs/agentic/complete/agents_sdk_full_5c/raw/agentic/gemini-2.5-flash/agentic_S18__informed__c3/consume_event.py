from messaging_client import get_subscriber_client, get_project_id
from messaging_models import PubSubMessage

def consume_event(subscription_id: str, timeout: float = 5.0):
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(request={
        "subscription": subscription_path,
        "max_messages": 1,
    }, retry=None)

    if not response.received_messages:
        print("No messages received.")
        return None, None

    for received_message in response.received_messages:
        message = PubSubMessage.from_pubsub_message(received_message.message)
        print(f"Received message: {message.data}")
        # Acknowledge the message for successful processing
        subscriber.acknowledge(request={
            "subscription": subscription_path,
            "ack_ids": [received_message.ack_id]
        })
        return message, received_message.ack_id

    return None, None
