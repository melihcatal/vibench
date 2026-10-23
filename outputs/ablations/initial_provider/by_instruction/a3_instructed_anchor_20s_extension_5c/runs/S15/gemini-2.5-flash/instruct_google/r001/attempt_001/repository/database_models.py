import json

class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def to_json(self):
        return json.dumps({"id": self.id, "data": self.data})