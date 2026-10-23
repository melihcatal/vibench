import json

class Document:
    def __init__(self, id: str, data: dict):
        self.id = id
        self.data = data

    def to_dict(self):
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, doc_id: str, doc_data: dict):
        return cls(doc_id, doc_data)

class UpsertDocumentRequest:
    def __init__(self, collection_name: str, document_id: str, document_data: dict):
        self.collection_name = collection_name
        self.document_id = document_id
        self.document_data = document_data

class UpsertDocumentResponse:
    def __init__(self, success: bool, document_id: str, message: str = ""):
        self.success = success
        self.document_id = document_id
        self.message = message
