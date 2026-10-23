class DocumentRequest:
    def __init__(self, document_type, document_bytes):
        self.document_type = document_type
        self.document_bytes = document_bytes

class DocumentResponse:
    def __init__(self, fields):
        self.fields = fields