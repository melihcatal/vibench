class Message:
    def __init__(self, body, attributes):
        self.body = body
        self.attributes = attributes


class PublishResponse:
    def __init__(self, message_id, sequence_number):
        self.message_id = message_id
        self.sequence_number = sequence_number
