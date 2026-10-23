class Message:
    def __init__(self, body):
        self.body = body

class PublishResponse:
    def __init__(self, message_id):
        self.message_id = message_id