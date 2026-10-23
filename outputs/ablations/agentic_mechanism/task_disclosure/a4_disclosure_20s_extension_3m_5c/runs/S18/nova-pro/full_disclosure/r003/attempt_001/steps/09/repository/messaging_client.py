from google.cloud import pubsub_v1


class MessagingClient:
    def __init__(self, project_id, topic_name):
        self.project_id = project_id
        self.topic_name = topic_name
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)
        self.subscription_path = self.subscriber.subscription_path(project_id, topic_name)

    def publish_message(self, data):
        future = self.publisher.publish(self.topic_path, data.encode('utf-8'))
        return future.result()

    def subscribe_message(self, callback):
        def message_callback(message):
            callback(message.data)
            message.ack()

        streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=message_callback)
        streaming_pull_future.result()


if __name__ == '__main__':
    project_id = 'your-project-id'
    topic_name = 'your-topic-name'
    client = MessagingClient(project_id, topic_name)
    data = 'Hello, Pub/Sub!'
    client.publish_message(data)
    print('Message published.')