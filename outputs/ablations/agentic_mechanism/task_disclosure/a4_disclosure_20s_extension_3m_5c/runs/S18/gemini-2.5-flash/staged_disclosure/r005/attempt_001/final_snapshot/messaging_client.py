from google.cloud import pubsub_v1
import os

class PubSubMessagingClient:
    def __init__(self, project_id: str = None):
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_name: str):
        return self.publisher.topic_path(self.project_id, topic_name)

    def get_subscription_path(self, subscription_name: str):
        return self.subscriber.subscription_path(self.project_id, subscription_name)

    def publish_message(self, topic_name: str, data: str, **attrs):
        topic_path = self.get_topic_path(topic_name)
        data = data.encode("utf-8")
        future = self.publisher.publish(topic_path, data, **attrs)
        return future.result()

    def subscribe_message(self, subscription_name: str, callback):
        subscription_path = self.get_subscription_path(subscription_name)
        streaming_pull_future = self.subscriber.subscribe(subscription_path, callback=callback)
        print(f"Listening for messages on {subscription_path}")
        return streaming_pull_future

    def create_topic(self, topic_name: str):
        topic_path = self.get_topic_path(topic_name)
        topic = self.publisher.create_topic(request={"name": topic_path})
        print(f"Topic created: {topic.name}")
        return topic

    def create_subscription(self, topic_name: str, subscription_name: str):
        topic_path = self.get_topic_path(topic_name)
        subscription_path = self.get_subscription_path(subscription_name)
        subscription = self.subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
        print(f"Subscription created: {subscription.name}")
        return subscription
