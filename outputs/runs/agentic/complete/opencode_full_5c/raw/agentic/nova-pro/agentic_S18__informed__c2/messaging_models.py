class PubSubMessage:
    def __init__(self, data):
        self.data = data


class PubSubBatch:
    def __init__(self, messages):
        self.messages = messages
