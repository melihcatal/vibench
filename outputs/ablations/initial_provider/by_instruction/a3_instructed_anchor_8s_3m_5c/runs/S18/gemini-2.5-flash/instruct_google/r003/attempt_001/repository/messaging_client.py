from google.cloud import pubsub_v1
import os

class PubSubClientHelper:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.publisher_client = pubsub_v1.PublisherClient()
        self.subscriber_client = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        """Returns the full topic path for a given topic ID."""
        return self.publisher_client.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Returns the full subscription path for a given subscription ID."""
        return self.subscriber_client.subscription_path(self.project_id, subscription_id)

    def get_publisher_client(self) -> pubsub_v1.PublisherClient:
        """Returns an initialized Pub/Sub publisher client."""
        return self.publisher_client

    def get_subscriber_client(self) -> pubsub_v1.SubscriberClient:
        """Returns an initialized Pub/Sub subscriber client."""
        return self.subscriber_client


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not PROJECT_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        client_helper = PubSubClientHelper(PROJECT_ID)
        topic_path = client_helper.get_topic_path("my-test-topic")
        subscription_path = client_helper.get_subscription_path("my-test-subscription")
        print(f"Test Topic Path: {topic_path}")
        print(f"Test Subscription Path: {subscription_path}")
