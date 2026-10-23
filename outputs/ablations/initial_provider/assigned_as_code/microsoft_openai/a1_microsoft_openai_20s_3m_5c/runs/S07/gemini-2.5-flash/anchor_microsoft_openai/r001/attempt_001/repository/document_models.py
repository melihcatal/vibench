from typing import Any, Dict, List, Optional

class DocumentPayload:
    def __init__(self, document_bytes: bytes, mime_type: str):
        self.document_bytes = document_bytes
        self.mime_type = mime_type

class AnalyzeResult:
    def __init__(self, result: Any):
        self._result = result

    @property
    def content(self) -> str:
        return self._result.content if self._result.content else ""

    @property
    def pages(self) -> List[Any]:
        return self._result.pages if self._result.pages else []

    @property
    def paragraphs(self) -> List[Any]:
        return self._result.paragraphs if self._result.paragraphs else []

    @property
    def tables(self) -> List[Any]:
        return self._result.tables if self._result.tables else []

    @property
    def key_value_pairs(self) -> List[Any]:
        return self._result.key_value_pairs if self._result.key_value_pairs else []

    @property
    def styles(self) -> List[Any]:
        return self._result.styles if self._result.styles else []

    @property
    def languages(self) -> List[Any]:
        return self._result.languages if self._result.languages else []

    @property
    def entities(self) -> List[Any]:
        return self._result.entities if self._result.entities else []
