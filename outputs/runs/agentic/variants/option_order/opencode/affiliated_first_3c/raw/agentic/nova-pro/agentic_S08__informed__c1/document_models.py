from typing import Dict


class DocumentRequest:
    def __init__(self, document: bytes):
        self.document = document


class DocumentResponse:
    def __init__(self, fields: Dict):
        self.fields = fields


def normalize_response(response: Dict) -> Dict:
    return response
