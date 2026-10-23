import os
from google.cloud import pubsub_v1
from google.oauth2 import service_account


def get_pubsub_client():
    """Get Google Cloud Pub/Sub publisher client with project ID."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        publisher = pubsub_v1.PublisherClient(credentials=credentials)
    else:
        publisher = pubsub_v1.PublisherClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project-id")
    return publisher, project_id


def get_pubsub_subscriber():
    """Get Google Cloud Pub/Sub subscriber client with project ID."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    else:
        subscriber = pubsub_v1.SubscriberClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project-id")
    return subscriber, project_id


def get_topic_path(topic_id: str) -> str:
    """Get full topic path from topic ID."""
    publisher, project_id = get_pubsub_client()
    return publisher.topic_path(project_id, topic_id)


def get_subscription_path(subscription_id: str) -> str:
    """Get full subscription path from subscription ID."""
    subscriber, project_id = get_pubsub_subscriber()
    return subscriber.subscription_path(project_id, subscription_id)


def validate_message_structure(message_data: dict) -> bool:
    """Validate that message has required fields."""
    required_fields = ["event_type", "customer_id", "timestamp"]
    return all(field in message_data for field in required_fields)
