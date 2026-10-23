from google.cloud import pubsub_v1

class PubSubRequest:
    def __init__(self, topic_name, message_data):
        self.topic_name = topic_name
        self.message_data = message_data

    def publish(self):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path('your-project-id', self.topic_name)
        data = self.message_data.encode('utf-8')
        publisher.publish(topic_path, data)

class PubSubResponse:
    def __init__(self, message):
        self.message = message

    def ack(self):
        pass  # Implement acknowledgment logic here

def normalize_message(message):
    return message.data.decode('utf-8')