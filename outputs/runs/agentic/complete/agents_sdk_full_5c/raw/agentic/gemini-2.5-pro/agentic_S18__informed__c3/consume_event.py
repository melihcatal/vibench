
import os
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, project_id, subscription_id

def consume_one_message():
    """Consumes a single message from a Google Cloud Pub/Sub subscription."""
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    print(f"Listening for messages on {subscription_path}..\n")

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        retry=None,
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    ack_ids = []
    received_message = response.received_messages[0]
    print(f"Received: {received_message.message.data.decode('utf-8')}")
    ack_ids.append(received_message.ack_id)

    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": ack_ids}
    )

    print(f"Acknowledged message: {received_message.message.message_id}")
    return received_message

if __name__ == '__main__':
    # This is an example, not part of the required functionality.
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        consume_one_message()
