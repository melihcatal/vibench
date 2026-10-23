class Event:
    def __init__(self, body):
        self.body = body

    def to_json(self):
        return {"body": self.body}

    @staticmethod
    def from_json(json_obj):
        return Event(json_obj["body"])