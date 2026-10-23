import json

class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def to_dict(self):
        return {'id': self.id, **self.data}

    @staticmethod
    def from_dict(doc_dict):
        doc_id = doc_dict.pop('id', None)
        return Document(doc_id, doc_dict)

class QueryResult:
    def __init__(self, documents):
        self.documents = documents

    def to_json(self):
        return json.dumps([doc.to_dict() for doc in self.documents], indent=2)
