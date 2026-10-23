class PubSubMessage:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return {"data": self.data}


class PubSubResponse:
    def __init__(self, message_id):
        self.message_id = message_id

    def to_json(self):
        return {"message_id": self.message_id}
