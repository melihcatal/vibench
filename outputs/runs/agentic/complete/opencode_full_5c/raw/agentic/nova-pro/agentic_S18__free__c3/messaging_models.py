class MessageRequest:
    def __init__(self, body, attributes):
        self.body = body
        self.attributes = attributes


class MessageResponse:
    def __init__(self, message_id, message_attributes):
        self.message_id = message_id
        self.message_attributes = message_attributes
