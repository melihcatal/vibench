class Document:
    def __init__(self, document_id: str, data: dict):
        self.document_id = document_id
        self.data = data

    def to_dict(self):
        return {"id": self.document_id, "data": self.data}

    @staticmethod
    def from_dict(document_id: str, source: dict):
        return Document(document_id, source)
