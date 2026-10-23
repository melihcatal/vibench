
from google.cloud import pubsub_v1

def consume_one_message(project_id: str, subscription_id: str):
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    print(f"Listening for messages on {subscription_path}...")

    # The subscriber pulls one message at a time.
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=30.0  # seconds
    )

    if response.received_messages:
        for received_message in response.received_messages:
            message = received_message.message
            print(f"Received message: {message.data.decode('utf-8')}")
            print(f"Message ID: {message.message_id}")

            # Acknowledge the message so it's not redelivered.
            ack_ids = [received_message.ack_id]
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
            print(f"Acknowledged message {message.message_id}")
    else:
        print("No messages received.")

    subscriber.close()

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Subscription ID
    # For example: project_id = "your-gcp-project-id"
    # For example: subscription_id = "your-pubsub-subscription-id"
    PROJECT_ID = "your-gcp-project-id"  # <<< IMPORTANT: Replace with your actual GCP Project ID
    SUBSCRIPTION_ID = "your-pubsub-subscription-id" # <<< IMPORTANT: Replace with your actual Pub/Sub Subscription ID

    if PROJECT_ID == "your-gcp-project-id" or SUBSCRIPTION_ID == "your-pubsub-subscription-id":
        print("Please update PROJECT_ID and SUBSCRIPTION_ID with your actual Google Cloud Pub/Sub details.")
    else:
        consume_one_message(PROJECT_ID, SUBSCRIPTION_ID)
