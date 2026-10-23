from google.cloud import pubsub_v1


class MessagingClient:
    def __init__(self, project_id, topic_name):
        self.project_id = project_id
        self.topic_name = topic_name
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish_message(self, data):
        data = data.encode("utf-8")
        future = self.publisher.publish(self.topic_path, data)
        print(f'Published message ID: {future.result()}')

    def create_topic(self):
        try:
            self.publisher.create_topic(request={"name": self.topic_path})
            print(f'Topic {self.topic_name} created.')
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    project_id = 'your-project-id'
    topic_name = 'your-topic-name'
    client = MessagingClient(project_id, topic_name)
    client.create_topic()
    client.publish_message('Hello, World!')