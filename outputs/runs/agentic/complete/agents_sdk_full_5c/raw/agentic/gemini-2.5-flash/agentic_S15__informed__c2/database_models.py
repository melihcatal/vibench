import json

class Document:
    def __init__(self, id: str, data: dict):
        self.id = id
        self.data = data

    def to_dict(self):
        return self.data

    @staticmethod
    def from_firestore_document(doc):
        return Document(doc.id, doc.to_dict())

class DocumentQuery:
    def __init__(self, field: str, value: any):
        self.field = field
        self.value = value

    def to_json(self):
        return json.dumps({"field": self.field, "value": self.value})
