from google.cloud import pubsub_v1
import os

def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient."""
    return pubsub_v1.SubscriberClient()

def get_topic_path(publisher_client, project_id: str, topic_id: str) -> str:
    """Constructs a Pub/Sub topic path."""
    return publisher_client.topic_path(project_id, topic_id)

def get_subscription_path(subscriber_client, project_id: str, subscription_id: str) -> str:
    """Constructs a Pub/Sub subscription path."""
    return subscriber_client.subscription_path(project_id, subscription_id)

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    TOPIC_ID = "test-topic-helper"
    SUBSCRIPTION_ID = "test-subscription-helper"

    publisher = get_publisher_client()
    topic_path = get_topic_path(publisher, PROJECT_ID, TOPIC_ID)
    print(f"Publisher client created. Example topic path: {topic_path}")

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscriber, PROJECT_ID, SUBSCRIPTION_ID)
    print(f"Subscriber client created. Example subscription path: {subscription_path}")
