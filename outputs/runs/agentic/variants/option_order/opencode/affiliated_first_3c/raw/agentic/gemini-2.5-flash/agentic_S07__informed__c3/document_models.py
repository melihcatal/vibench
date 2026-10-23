class DocumentExtractionRequest:
    def __init__(self, content: bytes, mime_type: str):
        self.content = content
        self.mime_type = mime_type


class DocumentExtractionResponse:
    def __init__(self, text: str = None, entities: list = None, document_obj=None):
        self.text = text
        self.entities = entities
        self.document_obj = document_obj  # Raw document object from provider
