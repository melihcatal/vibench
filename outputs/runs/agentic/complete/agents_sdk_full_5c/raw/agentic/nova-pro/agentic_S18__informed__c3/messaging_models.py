class PubSubMessage:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return {'data': self.data}