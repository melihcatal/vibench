from google.cloud import pubsub_v1


class MessagingClient:
    def __init__(self, project_id, topic_id, subscription_id):
        self.project_id = project_id
        self.topic_id = topic_id
        self.subscription_id = subscription_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish_message(self, data):
        topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
        future = self.publisher.publish(topic_path, data.encode('utf-8'))
        print(f'Published message ID: {future.result()}')

    def subscribe_to_messages(self):
        subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)

        def callback(message):
            print(f'Received message: {message.data.decode(