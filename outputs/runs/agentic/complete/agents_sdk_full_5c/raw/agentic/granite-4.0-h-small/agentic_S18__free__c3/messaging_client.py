import os
from google.cloud import pubsub_v1

# Environment variable for GCP project ID (override if needed)
PROJECT_ID = os.getenv('GCLOUD_PROJECT', 'your-gcp-project-id')

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """Create and return a PublisherClient for Pub/Sub."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Create and return a SubscriberClient for Pub/Sub."""
    return pubsub_v1.SubscriberClient()

# Example: allow custom project via env var
if __name__ == '__main__':
    pub = get_publisher_client()
    print(f"Publisher client ready for project {PROJECT_ID}")
    sub = get_subscriber_client()
    print(f"Subscriber client ready for project {PROJECT_ID}")
