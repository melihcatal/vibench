class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def from_dynamodb_item(item):
        return Document(item["id"], item)

    def to_dynamodb_item(self):
        return {"id": self.id, **self.data}
