from typing import List, Dict, Any, Optional

class DocumentInput:
    def __init__(self, s3_bucket: str, s3_key: str):
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

class ExtractionResult:
    def __init__(self(self, text: Optional[str] = None, layout: Optional[List[Dict[str, Any]]] = None, tables: Optional[List[Dict[str, Any]]] = None, key_values: Optional[List[Dict[str, Any]]] = None, raw_response: Optional[Dict[str, Any]] = None):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.key_values = key_values
        self.raw_response = raw_response

class TranslatedText:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

class SafetyResult:
    def __init__(self, unsafe_content_detected: bool, details: Dict[str, Any]):
        self.unsafe_content_detected = unsafe_content_detected
        self.details = details

class FieldExtractionResult:
    def __init__(self, extracted_fields: Dict[str, Any]):
        self.extracted_fields = extracted_fields

class EmbeddingResult:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding
