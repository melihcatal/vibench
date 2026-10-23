from pymongo import DESCENDING


class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def to_dict(self):
        return {"_id": self.id, **self.data}

    @staticmethod
    def from_dict(doc):
        return Document(doc["_id"], {k: v for k, v in doc.items() if k != "_id"})
