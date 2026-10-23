from google.cloud import pubsub_v1
import os
import json
import time

def consume_one_message(project_id: str, subscription_id: str, timeout: float = 5.0):
    """Consumes one message from a Pub/Sub subscription and acknowledges it."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    print(f"Listening for messages on {subscription_path}...")

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=timeout,
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]
    message_data = received_message.message.data.decode("utf-8")
    message_id = received_message.message.message_id
    ack_id = received_message.ack_id

    print(f"Received message ID: {message_id}")
    print(f"Data: {message_data}")

    # Acknowledge the message so it is not redelivered.
    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [ack_id]})
    print(f"Acknowledged message ID: {message_id}")

    subscriber.close()
    return json.loads(message_data)

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "my-json-events-subscription")

    consumed_event = consume_one_message(PROJECT_ID, SUBSCRIPTION_ID)
    if consumed_event:
        print("Successfully consumed and acknowledged an event.")
