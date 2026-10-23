from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class StorageObject:
    bucket: str
    key: str


@dataclass
class ObjectMetadata:
    key: str
    version_id: Optional[str]
    size: Optional[int]
    last_modified: Optional[str]
    content_type: Optional[str]
    etag: Optional[str]
    metadata: Optional[Dict[str, str]]


@dataclass
class OCRResult:
    text: str
    confidence: float


@dataclass
class TranslationResult:
    source_language: str
    translated_text: str


@dataclass
class SummaryResult:
    summary: str


@dataclass
class EmbeddingResult:
    embedding: List[float]
