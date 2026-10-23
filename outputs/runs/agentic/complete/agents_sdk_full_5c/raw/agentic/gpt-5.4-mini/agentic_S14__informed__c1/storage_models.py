from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class StorageConfig:
    bucket_name: str
    project_id: Optional[str] = None
    credentials_path: Optional[str] = None
    default_prefix: str = ""


@dataclass(frozen=True)
class ObjectIdentifier:
    bucket_name: str
    object_name: str


@dataclass(frozen=True)
class UploadRequest:
    bucket_name: Optional[str]
    object_name: str
    content_type: Optional[str] = None


@dataclass(frozen=True)
class PresignedDownloadRequest:
    bucket_name: Optional[str]
    object_name: str
    expiration_seconds: int = 3600


@dataclass(frozen=True)
class PrefixListRequest:
    bucket_name: Optional[str]
    prefix: str = ""
    delimiter: Optional[str] = None


@dataclass(frozen=True)
class MetadataResult:
    bucket_name: str
    object_name: str
    content_type: Optional[str]
    content_length: Optional[int]
    md5_hash: Optional[str]
    generation: Optional[str]
    updated: Optional[str]
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class ListResult:
    bucket_name: str
    prefix: str
    objects: List[str]


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: Optional[float]
    source_object: ObjectIdentifier


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class SummaryResult:
    summary: str
    source_text: str


@dataclass(frozen=True)
class EmbeddingResult:
    vector: List[float]
    source_text: str
    source_object: ObjectIdentifier


def normalize_text_blocks(blocks: Iterable[str]) -> str:
    return "\n".join(part.strip() for part in blocks if part and part.strip())
