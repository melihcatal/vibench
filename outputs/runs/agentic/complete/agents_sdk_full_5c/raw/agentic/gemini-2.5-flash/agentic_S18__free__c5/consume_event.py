from google.cloud import pubsub_v1
import os
import json

def consume_one_message(project_id: str, subscription_id: str):
    """Consumes one message from a Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # The subscriber pulls messages synchronously. This is suitable for consuming a single message.
    # Setting max_messages to 1 for consuming one message at a time.
    response = subscriber.pull(request={
        "subscription": subscription_path,
        "max_messages": 1,
    })

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]
    message_data = received_message.message.data.decode("utf-8")
    message_attributes = dict(received_message.message.attributes)
    ack_id = received_message.ack_id

    print(f"Received message: {message_data}")
    print(f"Attributes: {message_attributes}")

    # Acknowledge the message so it's not redelivered
    subscriber.acknowledge(request={
        "subscription": subscription_path,
        "ack_ids": [ack_id],
    })
    print(f"Acknowledged message with ack_id: {ack_id}")

    return {"data": json.loads(message_data), "attributes": message_attributes, "ack_id": ack_id}

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    SUBSCRIPTION_ID = "my-json-events-subscription" # Ensure this subscription exists in your GCP project

    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        consume_one_message(PROJECT_ID, SUBSCRIPTION_ID)
