from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class DocumentTextractFeature:
    feature_type: str # e.g., "FORMS", "TABLES", "LAYOUT"

@dataclass
class DocumentTextractRequest:
    document_content_bytes: bytes = field(default=None) # Raw image bytes
    s3_bucket: str = field(default=None)
    s3_key: str = field(default=None)
    features: List[DocumentTextractFeature] = field(default_factory=list)

@dataclass
class DocumentTextractResponse:
    text: str = ""
    key_values: Dict[str, str] = field(default_factory=dict)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    layout: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TranslationRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclass
class TranslationResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str

@dataclass
class SafetyRequest:
    text: str

@dataclass
class SafetyResponse:
    is_safe: bool
    moderation_labels: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FieldExtractionRequest:
    document_text: str
    # Add more fields as needed for specific extraction rules or model parameters

@dataclass
class FieldExtractionResponse:
    extracted_fields: Dict[str, Any] = field(default_factory=dict)
    raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EmbeddingRequest:
    text_segments: List[str]

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)
