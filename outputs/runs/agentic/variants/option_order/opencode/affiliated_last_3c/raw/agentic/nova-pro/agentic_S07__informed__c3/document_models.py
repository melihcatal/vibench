from typing import Any, Dict


class DocumentRequest:
    def __init__(self, document_path: str):
        self.document_path = document_path


class DocumentResponse:
    def __init__(self, content: Dict[str, Any]):
        self.content = content


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return response
