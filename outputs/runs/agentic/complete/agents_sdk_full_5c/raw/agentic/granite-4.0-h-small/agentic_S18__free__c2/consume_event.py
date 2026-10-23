import os
import json
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the concrete provider
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
SUBSCRIPTION_ID = os.getenv('PUBSUB_SUBSCRIPTION_ID')

# Helper function to pull a single message from a subscription
def consume_event() -> dict:
    """Pull one message from a Pub/Sub subscription and return its payload.

    Returns:
        dict: The deserialized JSON payload of the message.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    # Pull a single message with ack deadline of 10 seconds
    response = subscriber.pull(subscription_path, max_messages=1, timeout=10.0)
    if not response.received_messages:
        return None  # No message available
    message = response.received_messages[0].message
    data = json.loads(message.data.decode('utf-8'))
    # Acknowledge the message immediately
    subscriber.acknowledge(subscription_path, [message.ack_id])
    return data

def main():
    msg = consume_event()
    if msg:
        print(f"Consumed message: {msg}")
    else:
        print("No message received.")

if __name__ == "__main__":
    main()