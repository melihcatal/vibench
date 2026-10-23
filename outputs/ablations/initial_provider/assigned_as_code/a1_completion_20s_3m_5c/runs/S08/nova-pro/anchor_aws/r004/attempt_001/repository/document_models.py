from typing import Dict

class DocumentRequest:
    def __init__(self, document_image: bytes):
        self.document_image = document_image

class DocumentResponse:
    def __init__(self, fields: Dict):
        self.fields = fields

class NormalizationHelper:
    @staticmethod
    def normalize_fields(fields: Dict) -> str:
        return json.dumps(fields, indent=2)