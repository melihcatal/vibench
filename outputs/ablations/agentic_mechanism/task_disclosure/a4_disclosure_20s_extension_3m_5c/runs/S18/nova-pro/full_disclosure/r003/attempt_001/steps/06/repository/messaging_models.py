from google.cloud import pubsub_v1


class PubSubRequest:
    def __init__(self, topic_name, message):
        self.topic_name = topic_name
        self.message = message

    def publish(self, project_id):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, self.topic_name)
        data = self.message.encode('utf-8')
        future = publisher.publish(topic_path, data)
        print(f'Published message ID: {future.result()}')


class PubSubResponse:
    def __init__(self, message):
        self.message = message

    def deserialize(self):
        return self.message.data.decode('utf-8')


def normalize_message(message):
    return message.lower()