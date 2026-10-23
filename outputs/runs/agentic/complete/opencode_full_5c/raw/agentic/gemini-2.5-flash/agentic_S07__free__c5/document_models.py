from typing import List, Dict, Any, Optional


class DocumentTextExtractionResponse:
    def __init__(self, text_content: str):
        self.text_content = text_content


class DocumentLayoutExtractionResponse:
    def __init__(self, layout_elements: List[Dict[str, Any]]):
        self.layout_elements = layout_elements


class DocumentTableExtractionResponse:
    def __init__(self, tables: List[Dict[str, Any]]):
        self.tables = tables


class DocumentKeyValueExtractionResponse:
    def __init__(self, key_value_pairs: Dict[str, Any]):
        self.key_value_pairs = key_value_pairs


class TranslatedTextResponse:
    def __init__(self, translated_text: str, detected_language: Optional[str] = None):
        self.translated_text = translated_text
        self.detected_language = detected_language


class SafetyCheckResponse:
    def __init__(self, safety_attributes: Dict[str, Any]):
        self.safety_attributes = safety_attributes


class FieldExtractionResponse:
    def __init__(self, fields: Dict[str, Any]):
        self.fields = fields


class OCREmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings
