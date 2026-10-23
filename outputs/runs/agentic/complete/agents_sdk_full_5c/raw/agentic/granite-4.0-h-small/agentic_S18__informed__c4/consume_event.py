import os
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client
from messaging_models import normalize_message

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
subscription_name = os.getenv('CONSUME_SUBSCRIPTION', 'my-subscription')

def consume_event():
    """Consume a single message from Google Cloud Pub/Sub subscription.

    Returns:
        dict: Normalized JSON payload if message exists, else None.
    """
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    # Pull one message (ack deadline set to default)
    try:
        response = subscriber.pull(subscription_path, max_messages=1)
        if not response.received_messages:
            print("No messages available.")
            return None
        message = response.received_messages[0]
        # Decode JSON payload
        payload_bytes = message.message.data
        payload = json.loads(payload_bytes.decode('utf-8'))
        # Normalize / transform if needed
        normalized = normalize_message(payload)
        # Acknowledge after processing
        subscriber.acknowledge(subscription_path, [message.ack_id])
        print(f"Consumed message ID: {message.message.message_id}")
        return normalized
    except Exception as e:
        print(f"Error consuming event: {e}")
        return None
