from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ObjectMetadata:
    """
    A normalized data model for object storage metadata.
    """
    name: str
    bucket: str
    size: int
    updated: datetime
    content_type: Optional[str] = None
    md5_hash: Optional[str] = None
    crc32c: Optional[str] = None

@dataclass
class OcrResult:
    """
    Represents the result of an OCR operation.
    """
    source_uri: str
    text_content: str
    language: Optional[str] = None

@dataclass
class TranslationResult:
    """
    Represents the result of a translation operation.
    """
    source_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class SummaryResult:
    """
    Represents the result of a summarization operation.
    """
    source_text_length: int
    summary_text: str
    model_id: str

@dataclass
class EmbeddingResult:
    """
    Represents the result of an embedding operation.
    """
    source_text: str
    embedding_vector: list[float]
    model_id: str
