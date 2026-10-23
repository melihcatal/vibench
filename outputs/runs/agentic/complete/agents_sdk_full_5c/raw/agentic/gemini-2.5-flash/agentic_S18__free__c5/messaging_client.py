from google.cloud import pubsub_v1
import os

def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient instance."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient instance."""
    return pubsub_v1.SubscriberClient()

def get_topic_path(project_id: str, topic_id: str) -> str:
    """Constructs and returns the full path for a Pub/Sub topic."""
    publisher = get_publisher_client()
    return publisher.topic_path(project_id, topic_id)

def get_subscription_path(project_id: str, subscription_id: str) -> str:
    """Constructs and returns the full path for a Pub/Sub subscription."""
    subscriber = get_subscriber_client()
    return subscriber.subscription_path(project_id, subscription_id)


if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    TOPIC_ID = "example-topic"
    SUBSCRIPTION_ID = "example-subscription"

    print(f"Publisher Client: {get_publisher_client()}")
    print(f"Subscriber Client: {get_subscriber_client()}")
    print(f"Example Topic Path: {get_topic_path(PROJECT_ID, TOPIC_ID)}")
    print(f"Example Subscription Path: {get_subscription_path(PROJECT_ID, SUBSCRIPTION_ID)}")
