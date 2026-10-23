class DocumentRequest:
    def __init__(self, document_path, model_id):
        self.document_path = document_path
        self.model_id = model_id

class DocumentResponse:
    def __init__(self, result):
        self.result = result