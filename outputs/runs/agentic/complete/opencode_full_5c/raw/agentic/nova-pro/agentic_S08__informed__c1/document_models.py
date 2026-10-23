class DocumentRequest:
    def __init__(self, document_path, service):
        self.document_path = document_path
        self.service = service


class DocumentResponse:
    def __init__(self, document):
        self.document = document
