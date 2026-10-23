from google.cloud import pubsub_v1

class PubSubRequest:
    def __init__(self, topic_name, message):
        self.topic_name = topic_name
        self.message = message

    @staticmethod
    def normalize_message(message):
        return message.encode('utf-8')

class PubSubResponse:
    def __init__(self, message_id):
        self.message_id = message_id

    @staticmethod
    def parse_response(response):
        return PubSubResponse(response.message_id)

def publish_message(request):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('my-project-id', request.topic_name)
    data = request.normalize_message(request.message)
    response = publisher.publish(topic_path, data)
    return PubSubResponse.parse_response(response)