# [HELPER] document_models.py

from typing import NamedTuple, List, Dict

# Normalized response structures for OCR and layout extraction

class TextExtractionResponse(NamedTuple):
    full_text: str

class LayoutExtractionResponse(NamedTuple):
    layout_entities: List[Dict]  # each dict holds type, bounding_box, etc.

class TableExtractionResponse(NamedTuple):
    tables: List[Dict]  # each dict contains layout and row/col dimensions

class KeyValueExtractionResponse(NamedTuple):
    key_value_pairs: List[Dict[str, str]]

class TranslationResponse(NamedTuple):
    translated_text: str

class SafetyResponse(NamedTuple):
    safe: bool
    flagged_categories: List[str]

class FieldExtractionResponse(NamedTuple):
    fields: Dict[str, str]

class EmbeddingResponse(NamedTuple):
    embeddings: List[List[float]]
