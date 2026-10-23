import os
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_project_id, get_subscription_path
from messaging_models import Event

def consume_one_message():
    """Consumes a single message from a Google Cloud Pub/Sub subscription."""
    project_id = get_project_id()
    subscription_id = os.getenv("GCP_PUBSUB_SUBSCRIPTION_ID", "my-subscription")

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscriber, project_id, subscription_id)

    print(f"Listening for messages on {subscription_path}...")

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        retry=None,
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]
    message_data = received_message.message.data.decode("utf-8")
    event = Event.from_json(message_data)
    
    print(f"Received event: {event}")

    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
    )
    print(f"Acknowledged message: {received_message.ack_id}")

    return event
