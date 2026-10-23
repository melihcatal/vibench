import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

def consume_event(project_id, subscription_name):
    """Consume a single message from a Pub/Sub subscription.

    Args:
        project_id (str): GCP project ID.
        subscription_name (str): Pub/Sub subscription name.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    subscriber = get_pubsub_client()
    subscription_path = f"projects/{project_id}/subscriptions/{subscription_name}"
    future = subscriber.subscribe(subscription_path, callback=receive_messages)
    # Run the subscriber until a shutdown signal is received
    try:
        # Should block forever; in this example we just wait 60 seconds to receive.
        future.result(timeout=60)
    except Exception as e:
        print(f"An error occurred while consuming: {e}")

def receive_messages(message):
    """Callback to handle received messages.",
    print(f"Received message: {message}")
    # Acknowledge the message
    message.ack()
    # If the processing fails, consider sending to dead letter
    # (handled elsewhere per requirement)
