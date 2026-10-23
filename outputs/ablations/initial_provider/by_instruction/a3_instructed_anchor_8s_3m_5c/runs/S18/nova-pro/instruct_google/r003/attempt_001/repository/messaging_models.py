class PubSubMessage:
    def __init__(self, data, attributes=None):
        self.data = data
        self.attributes = attributes or {}

    @staticmethod
    def from_dict(data):
        return PubSubMessage(data['data'], data.get('attributes', {}))