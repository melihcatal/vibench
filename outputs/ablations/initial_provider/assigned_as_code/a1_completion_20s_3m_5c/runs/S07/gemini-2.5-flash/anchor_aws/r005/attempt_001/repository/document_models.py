class DocumentPayload:
    def __init__(self, document_bytes: bytes):
        self.document_bytes = document_bytes

class ExtractionResult:
    def __init__(self, data: dict):
        self.data = data
