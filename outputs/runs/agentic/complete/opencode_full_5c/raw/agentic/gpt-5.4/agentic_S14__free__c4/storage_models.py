from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    object_key: str
    file_path: str | None = None
    data: bytes | None = None
    content_type: str | None = None
    metadata: dict[str, str] | None = None


@dataclass(slots=True)
class UploadObjectResponse:
    bucket: str
    object_key: str
    etag: str | None
    version_id: str | None
    checksum_sha256: str | None


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    object_key: str
    expires_in: int = 3600
    response_content_type: str | None = None


@dataclass(slots=True)
class PresignedDownloadResponse:
    bucket: str
    object_key: str
    url: str
    expires_in: int


@dataclass(slots=True)
class ObjectMetadataRequest:
    bucket: str
    object_key: str


@dataclass(slots=True)
class ObjectMetadataResponse:
    bucket: str
    object_key: str
    content_length: int | None
    content_type: str | None
    etag: str | None
    last_modified: str | None
    metadata: dict[str, str]
    version_id: str | None


@dataclass(slots=True)
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    max_keys: int = 100
    continuation_token: str | None = None


@dataclass(slots=True)
class ListedObject:
    object_key: str
    size: int
    etag: str | None
    last_modified: str | None


@dataclass(slots=True)
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list[ListedObject]
    next_continuation_token: str | None


@dataclass(slots=True)
class StoredDocumentOcrRequest:
    bucket: str
    object_key: str


@dataclass(slots=True)
class StoredDocumentOcrResponse:
    bucket: str
    object_key: str
    provider: str
    extracted_text: str
    pages: list[dict[str, Any]]


@dataclass(slots=True)
class StoredTextTranslateRequest:
    text: str
    target_language: str
    source_language: str | None = None


@dataclass(slots=True)
class StoredTextTranslateResponse:
    provider: str
    translated_text: str
    detected_source_language: str | None
    target_language: str


@dataclass(slots=True)
class StoredAssetSummaryRequest:
    text: str
    max_output_tokens: int = 300


@dataclass(slots=True)
class StoredAssetSummaryResponse:
    provider: str
    model: str
    summary: str


@dataclass(slots=True)
class AssetMetadataEmbeddingRequest:
    bucket: str
    object_key: str
    metadata: dict[str, Any]
    extracted_text: str


@dataclass(slots=True)
class AssetMetadataEmbeddingResponse:
    provider: str
    model: str
    vector: list[float]
    dimensions: int
    input_text: str


def normalize_datetime(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def compact_text(value: str, limit: int = 8000) -> str:
    normalized = " ".join(value.split())
    return normalized[:limit]


def build_embedding_input(
    bucket: str, object_key: str, metadata: dict[str, Any], extracted_text: str
) -> str:
    metadata_parts = [f"{key}={metadata[key]}" for key in sorted(metadata)]
    pieces = [f"bucket={bucket}", f"object_key={object_key}"]
    if metadata_parts:
        pieces.append("metadata=" + "; ".join(metadata_parts))
    if extracted_text:
        pieces.append("text=" + compact_text(extracted_text, 6000))
    return "\n".join(pieces)
