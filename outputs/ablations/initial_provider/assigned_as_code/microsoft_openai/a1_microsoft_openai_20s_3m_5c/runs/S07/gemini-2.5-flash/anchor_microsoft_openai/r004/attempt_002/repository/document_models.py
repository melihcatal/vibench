from typing import Dict, Any, List, Optional

class DocumentInput:
    def __init__(self, document_bytes: bytes, mime_type: str, filename: Optional[str] = None):
        self.document_bytes = document_bytes
        self.mime_type = mime_type
        self.filename = filename

class ExtractedText:
    def __init__(self, text: str):
        self.text = text

class ExtractedLayout:
    def __init__(self, pages: List[Dict[str, Any]]):
        self.pages = pages

class ExtractedTables:
    def __init__(self, tables: List[Dict[str, Any]]):
        self.tables = tables

class ExtractedKeyValues:
    def __init__(self, key_values: Dict[str, str]):
        self.key_values = key_values

class TranslatedText:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

class SafetyCheckResult:
    def __init__(self, is_safe: bool, scores: Dict[str, float]):
        self.is_safe = is_safe
        self.scores = scores

class DocumentFieldExtractionResult:
    def __init__(self, fields: Dict[str, Any]):
        self.fields = fields

class OCRFootprint:
    def __init__(self, provider: str, model: str, cost: float = 0.0):
        self.provider = provider
        self.model = model
        self.cost = cost

class DocumentEmbedding:
    def __init__(self, embedding: List[float], text_segment: str):
        self.embedding = embedding
        self.text_segment = text_segment
