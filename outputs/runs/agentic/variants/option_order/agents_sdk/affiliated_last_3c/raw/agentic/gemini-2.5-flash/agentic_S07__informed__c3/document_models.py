"""
Defines local request, response, and normalization helpers for OCR and Layout Extraction.
These are simple placeholder models for demonstration.
"""

class DocumentProcessingRequest:
    def __init__(self, document_url: str = None, document_content: bytes = None, content_type: str = None):
        self.document_url = document_url
        self.document_content = document_content
        self.content_type = content_type

class ExtractedTextResult:
    def __init__(self, text: str):
        self.text = text

class ExtractedLayoutResult:
    def __init__(self, pages: list):
        self.pages = pages # List of dicts or objects representing page layouts

class ExtractedTableResult:
    def __init__(self, tables: list):
        self.tables = tables # List of dicts or objects representing tables

class ExtractedKeyValueResult:
    def __init__(self, key_values: dict):
        self.key_values = key_values # Dict of extracted key-value pairs

class TranslatedTextResult:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

class ContentSafetyResult:
    def __init__(self, text_safety_results: list):
        self.text_safety_results = text_safety_results

class FieldExtractionResult:
    def __init__(self, fields: dict):
        self.fields = fields

class EmbeddingResult:
    def __init__(self, embedding: list):
        self.embedding = embedding
