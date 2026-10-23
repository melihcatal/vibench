from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class StorageObject:
    bucket: str
    key: str
    metadata: Dict[str, Any]


@dataclass
class PresignedUrl:
    url: str
    method: str


@dataclass
class OcrResult:
    text: str


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str


@dataclass
class SummaryResult:
    summary_text: str


@dataclass
class EmbeddingResult:
    embedding: List[float]
