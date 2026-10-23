import os
from typing import Dict, Any
from document_client import DocumentClient
from document_models import DocumentText


class TextExtractor:
    def __init__(self):
        self.client = DocumentClient()

    def extract_text(self, file_path: str) -> DocumentText:
        result = self.client.analyze_document(file_path)
        full_text = result.get("content", "")
        pages = [page.get("content", "") for page in result.get("pages", [])]
        confidence = self._calculate_confidence(result)
        return DocumentText(full_text=full_text, pages=pages, confidence=confidence)

    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        paragraphs = result.get("paragraphs", [])
        if not paragraphs:
            return 0.0
        total_confidence = sum(p.get("confidence", 0.0) for p in paragraphs)
        return total_confidence / len(paragraphs) if paragraphs else 0.0