
from google.cloud import pubsub_v1
import os

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
TOPIC_NAME = "my-topic"
SUBSCRIPTION_NAME = "my-subscription"

class PubSubClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_name: str) -> str:
        return self.publisher.topic_path(self.project_id, topic_name)

    def get_subscription_path(self, subscription_name: str) -> str:
        return self.subscriber.subscription_path(self.project_id, subscription_name)

    def publish_message(self, topic_name: str, message_data: str, **attrs):
        topic_path = self.get_topic_path(topic_name)
        data = message_data.encode("utf-8")
        future = self.publisher.publish(topic_path, data, **attrs)
        return future.result()

    def subscribe_messages(self, subscription_name: str, callback):
        subscription_path = self.get_subscription_path(subscription_name)
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path, callback=callback
        )
        print(f"Listening for messages on {subscription_path}...")
        return streaming_pull_future

# Example Usage (optional, for demonstration)
if __name__ == "__main__":
    # Replace with your actual project ID if not set in environment
    client = PubSubClient(PROJECT_ID)

    # Example callback for messages
    def message_callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    # To publish a message:
    # try:
    #     message_id = client.publish_message(TOPIC_NAME, "Hello Pub/Sub!", origin="python-client")
    #     print(f"Published message with ID: {message_id}")
    # except Exception as e:
    #     print(f"Error publishing message: {e}")

    # To subscribe to messages (this will block and listen):
    # You need to have a topic and subscription created in your GCP project
    # try:
    #     streaming_pull_future = client.subscribe_messages(SUBSCRIPTION_NAME, message_callback)
    #     with client.subscriber:
    #         try:
    #             streaming_pull_future.result()
    #         except TimeoutError:
    #             streaming_pull_future.cancel()
    #             streaming_pull_future.result()
    # except Exception as e:
    #     print(f"Error subscribing to messages: {e}")
