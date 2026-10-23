
from google.cloud import pubsub_v1
import os

class MessagingClient:
    def __init__(self, project_id=None):
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish_message(self, topic_id, message_data):
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        message_bytes = message_data.encode("utf-8")
        try:
            publish_future = self.publisher.publish(topic_path, message_bytes)
            publish_future.result()  # Verify the publication succeeded
            return f"Published message to {topic_path}"
        except Exception as e:
            return f"Failed to publish message: {e}"

    def subscribe_to_topic(self, subscription_id, callback):
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)

        streaming_pull_future = self.subscriber.subscribe(subscription_path, callback=callback)
        print(f"Listening for messages on {subscription_path}")

        # The subscriber is non-blocking, so we must keep the main thread from
        # exiting to allow it to process messages in the background.
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()

    def create_topic(self, topic_id):
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        try:
            topic = self.publisher.create_topic(request={"name": topic_path})
            return f"Topic {topic.name} created."
        except Exception as e:
            return f"Failed to create topic: {e}"

    def create_subscription(self, topic_id, subscription_id):
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        try:
            subscription = self.subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            return f"Subscription {subscription.name} created on topic {topic_id}."
        except Exception as e:
            return f"Failed to create subscription: {e}"

    def delete_topic(self, topic_id):
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        try:
            self.publisher.delete_topic(request={"topic": topic_path})
            return f"Topic {topic_id} deleted."
        except Exception as e:
            return f"Failed to delete topic: {e}"

    def delete_subscription(self, subscription_id):
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        try:
            self.subscriber.delete_subscription(request={"subscription": subscription_path})
            return f"Subscription {subscription_id} deleted."
        except Exception as e:
            return f"Failed to delete subscription: {e}"

