class DocumentRequest:
    def __init__(self, document_path):
        self.document_path = document_path


class DocumentResponse:
    def __init__(self, fields):
        self.fields = fields
