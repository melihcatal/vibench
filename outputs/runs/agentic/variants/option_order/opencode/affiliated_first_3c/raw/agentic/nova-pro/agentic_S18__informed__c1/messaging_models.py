class EventMessage:
    def __init__(self, message, attributes):
        self.message = message
        self.attributes = attributes


class DeadLetterMessage:
    def __init__(self, message, attributes):
        self.message = message
        self.attributes = attributes
