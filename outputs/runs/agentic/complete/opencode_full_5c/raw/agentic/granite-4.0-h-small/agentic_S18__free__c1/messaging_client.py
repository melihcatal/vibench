import os
from google.cloud import pubsub_v1

class MessagingClient:
    """Local helper that creates configured Pub/Sub client objects.

    The concrete provider is Google Cloud Pub/Sub, identified by the import
    `google.cloud.pubsub_v1` and the usage of `PublisherClient` / `SubscriberClient`."
    def __init__(self):
        # Load Project ID from environment (required by Google Cloud libraries)
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "default-project")
        # Initialize publisher and subscriber clients
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
