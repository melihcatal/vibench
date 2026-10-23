from google.cloud import pubsub_v1


class PubSubRequest:
    def __init__(self, topic_name, data):
        self.topic_name = topic_name
        self.data = data

    def to_dict(self):
        return {
            'topic_name': self.topic_name,
            'data': self.data
        }


class PubSubResponse:
    def __init__(self, message_id):
        self.message_id = message_id

    def to_dict(self):
        return {
            'message_id': self.message_id
        }


def normalize_message(message):
    if isinstance(message, pubsub_v1.types.PubsubMessage):
        return message.data.decode('utf-8')
    return message