from typing import List, Dict, Any


class DocumentExtractionResult:
    def __init__(
        self,
        text_content: str = "",
        layout_elements: List[Dict] = None,
        tables: List[Dict] = None,
        key_values: List[Dict] = None,
    ):
        self.text_content = text_content
        self.layout_elements = layout_elements if layout_elements is not None else []
        self.tables = tables if tables is not None else []
        self.key_values = key_values if key_values is not None else []


class OCRTranslationRequest:
    def __init__(self, text: str, target_language: str):
        self.text = text
        self.target_language = target_language


class OCRTranslationResult:
    def __init__(self, translated_text: str, source_language: str = None):
        self.translated_text = translated_text
        self.source_language = source_language


class OCRSafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text


class OCRSafetyCheckResult:
    def __init__(self, is_safe: bool, moderation_details: Dict[str, Any] = None):
        self.is_safe = is_safe
        self.moderation_details = (
            moderation_details if moderation_details is not None else {}
        )


class DocumentFieldExtractionRequest:
    def __init__(self, document_content: bytes, mime_type: str):
        self.document_content = document_content
        self.mime_type = mime_type


class DocumentFieldExtractionResult:
    def __init__(self, fields: Dict[str, Any]):
        self.fields = fields


class OCREmbeddingRequest:
    def __init__(self, text_sections: List[str]):
        self.text_sections = text_sections


class OCREmbeddingResult:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings
