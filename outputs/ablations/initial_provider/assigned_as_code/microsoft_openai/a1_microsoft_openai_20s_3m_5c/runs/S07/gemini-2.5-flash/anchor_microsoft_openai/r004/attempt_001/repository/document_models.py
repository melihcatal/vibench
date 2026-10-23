from typing import Dict, Any, List

class DocumentAnalysisRequest:
    document_bytes: bytes
    mime_type: str

    def __init__(self, document_bytes: bytes, mime_type: str):
        self.document_bytes = document_bytes
        self.mime_type = mime_type

class DocumentAnalysisResponse:
    content: str
    pages: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    key_value_pairs: List[Dict[str, Any]]
    languages: List[Dict[str, Any]]

    def __init__(self, **kwargs):
        self.content = kwargs.get("content", "")
        self.pages = kwargs.get("pages", [])
        self.tables = kwargs.get("tables", [])
        self.key_value_pairs = kwargs.get("key_value_pairs", [])
        self.languages = kwargs.get("languages", [])
