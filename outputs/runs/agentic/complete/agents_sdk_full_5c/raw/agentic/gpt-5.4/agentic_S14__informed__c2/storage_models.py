from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, BinaryIO, Iterable, Mapping


@dataclass(slots=True)
class ObjectRef:
    bucket: str
    key: str


@dataclass(slots=True)
class UploadRequest:
    bucket: str
    key: str
    data: bytes | BinaryIO | str
    content_type: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UploadResult:
    bucket: str
    key: str
    etag: str | None
    version_id: str | None = None
    provider: str = "amazon_s3"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PresignedDownload:
    bucket: str
    key: str
    url: str
    expires_in: int
    provider: str = "amazon_s3"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    size: int | None
    etag: str | None
    content_type: str | None
    last_modified: str | None
    metadata: dict[str, str] = field(default_factory=dict)
    storage_class: str | None = None
    provider: str = "amazon_s3"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int | None
    etag: str | None
    last_modified: str | None
    storage_class: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: list[ListedObject]
    continuation_token: str | None = None
    provider: str = "amazon_s3"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["objects"] = [obj.to_dict() for obj in self.objects]
        return payload


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    document_text: str
    page_count: int
    provider: str = "amazon_textract"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str | None
    target_language: str
    provider: str = "amazon_translate"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str
    provider: str = "openai"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    model: str
    dimensions: int
    provider: str = "openai"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def isoformat_or_none(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    text = str(value)
    return text if text else None


def normalize_metadata(metadata: Mapping[str, Any] | None) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items()}


def flatten_lines(lines: Iterable[str]) -> str:
    return "\n".join(line.strip() for line in lines if line and line.strip())
