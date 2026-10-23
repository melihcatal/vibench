from .document_client import DocumentClient


class DocumentModels:
    def __init__(self):
        self.client = DocumentClient()

    def normalize_response(self, response):
        return response
