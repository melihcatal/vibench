class DocumentRequest:
    def __init__(self, document_path):
        self.document_path = document_path

class DocumentResponse:
    def __init__(self, extracted_fields):
        self.extracted_fields = extracted_fields