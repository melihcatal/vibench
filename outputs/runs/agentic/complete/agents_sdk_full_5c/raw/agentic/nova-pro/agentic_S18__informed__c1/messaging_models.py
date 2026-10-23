class Message:
    def __init__(self, content, attributes=None):
        self.content = content
        self.attributes = attributes or {}

class Event:
    def __init__(self, message, topic_arn):
        self.message = message
        self.topic_arn = topic_arn