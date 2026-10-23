import os
from google.cloud import pubsub_v1

# --- Configuration ---
# Replace with your Google Cloud Project ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id") 

# Replace with your Pub/Sub topic name
TOPIC_NAME = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC", "your-pubsub-topic-name")

# Replace with your Pub/Sub subscription name (for subscribers)
SUBSCRIPTION_NAME = os.getenv("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION", "your-pubsub-subscription-name")

# --- Client Helper Utilities ---

def publish_message(message_data: str, project_id: str = PROJECT_ID, topic_name: str = TOPIC_NAME):
    """Publishes a message to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    
    # Data must be a bytestring
    data = message_data.encode("utf-8")
    
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

def subscribe_messages(project_id: str = PROJECT_ID, subscription_name: str = SUBSCRIPTION_NAME, timeout: int = 60):
    """Receives messages from a Google Cloud Pub/Sub subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
