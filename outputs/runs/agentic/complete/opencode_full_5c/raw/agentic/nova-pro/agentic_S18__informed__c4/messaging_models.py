class Message:
    def __init__(self, body, attributes=None):
        self.body = body
        self.attributes = attributes or {}

    def to_dict(self):
        return {"body": self.body, "attributes": self.attributes}
