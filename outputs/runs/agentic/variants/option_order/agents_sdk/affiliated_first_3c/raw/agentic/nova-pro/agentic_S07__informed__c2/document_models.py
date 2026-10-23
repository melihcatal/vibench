class DocumentModel:
    def __init__(self, document_path):
        self.document_path = document_path

    def to_bytes(self):
        with open(self.document_path, 'rb') as document:
            return document.read()