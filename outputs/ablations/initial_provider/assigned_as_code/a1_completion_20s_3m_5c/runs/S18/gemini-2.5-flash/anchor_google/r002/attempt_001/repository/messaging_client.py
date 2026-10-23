from google.cloud import pubsub_v1

class PubSubClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str):
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str):
        return self.subscriber.subscription_path(self.project_id, subscription_id)
