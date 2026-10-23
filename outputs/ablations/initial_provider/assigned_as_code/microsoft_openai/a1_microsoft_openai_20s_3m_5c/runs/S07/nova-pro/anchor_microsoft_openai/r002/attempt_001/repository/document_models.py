class DocumentRequest:
    def __init__(self, document_bytes, mime_type):
        self.document_bytes = document_bytes
        self.mime_type = mime_type

class DocumentResponse:
    def __init__(self, content):
        self.content = content