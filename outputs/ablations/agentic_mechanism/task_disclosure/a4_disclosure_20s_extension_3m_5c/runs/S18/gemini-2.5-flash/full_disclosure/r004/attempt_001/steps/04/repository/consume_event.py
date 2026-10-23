from google.cloud import pubsub_v1
import os

def consume_one_message(project_id: str, subscription_id: str):
    """Consumes one message from a Pub/Sub subscription."""
    
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=30.0,
    )

    if response.received_messages:
        for received_message in response.received_messages:
            print(f"Received message: {received_message.message.data.decode('utf-8')}")
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
            )
            print(f"Acknowledged message: {received_message.ack_id}")
            return received_message.message.data.decode('utf-8')
    else:
        print("No messages received.")
        return None

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Subscription ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    subscription_id = os.environ.get("GOOGLE_CLOUD_SUBSCRIPTION_ID")

    if not project_id or not subscription_id:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_SUBSCRIPTION_ID environment variables.")
    else:
        consume_one_message(project_id, subscription_id)
