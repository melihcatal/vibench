import json
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client
from messaging_models import MessagePayload

PROJECT_ID = 'your-gcp-project-id'
SUBSCRIPTION_ID = 'your-subscription-id'

def consume_event(timeout_seconds: int = 10):
    """Consume a single message from a Pub/Sub subscription.

    Args:
        timeout_seconds (int): How long to wait for a message.
    """
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    response = subscriber.pull(subscription_path, max_messages=1, timeout=timeout_seconds)
    if not response.received_messages:
        print("No messages received.")
        return None
    message = response.received_messages[0]
    # Acknowledge the message after processing
    subscriber.acknowledge(subscription_path, [message.ack_id])
    # Parse the JSON payload
    data = json.loads(message.message.data.decode('utf-8'))
    payload = MessagePayload(**data)
    print(f"Consumed event {payload.event_id}: {payload}")
    return payload

if __name__ == '__main__':
    consume_event(timeout_seconds=5)
