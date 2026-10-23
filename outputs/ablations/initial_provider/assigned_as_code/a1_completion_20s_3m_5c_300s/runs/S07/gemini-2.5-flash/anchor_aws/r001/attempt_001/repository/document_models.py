from typing import Dict, Any, List

class Document:
    def __init__(self, document_bytes: bytes):
        self.document_bytes = document_bytes

class ExtractedText:
    def __init__(self, text: str):
        self.text = text

class ExtractedLayout:
    def __init__(self, blocks: List[Dict[str, Any]]):
        self.blocks = blocks

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

class SafetyResult:
    def __init__(self, safe: bool, moderation_labels: List[Dict[str, Any]]):
        self.safe = safe
        self.moderation_labels = moderation_labels

class DocumentFields:
    def __init__(self, fields: Dict[str, Any]):
        self.fields = fields

class TextEmbedding:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding
