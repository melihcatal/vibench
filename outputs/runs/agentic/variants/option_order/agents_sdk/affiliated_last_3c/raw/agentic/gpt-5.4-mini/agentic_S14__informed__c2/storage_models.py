from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: bytes
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    etag: Optional[str] = None
    size: Optional[int] = None
    last_modified: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class ListedObject:
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    is_truncated: Optional[bool] = None


@dataclass
class OCRResult:
    source_bucket: str
    source_key: str
    text: str
    language: Optional[str] = None
    provider: str = "amazon-textract"


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = "amazon-translate"


@dataclass
class SummaryResult:
    source_text: str
    summary: str
    model_id: str
    provider: str = "anthropic"


@dataclass
class EmbeddingResult:
    object_key: str
    embedding: List[float]
    provider: str = "openai"
    model: str = "text-embedding-3-small"


def isoformat(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.astimezone(timezone.utc).isoformat()


def normalize_mapping(values: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not values:
        return {}
    return {str(k): str(v) for k, v in values.items()}


def to_dict(instance: Any) -> Dict[str, Any]:
    return asdict(instance)
