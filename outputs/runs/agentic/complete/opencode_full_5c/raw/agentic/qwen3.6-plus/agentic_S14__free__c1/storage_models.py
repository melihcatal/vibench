from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class UploadRequest:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"
    server_side_encryption: Optional[str] = None


@dataclass
class UploadResponse:
    etag: str
    version_id: Optional[str]
    bucket: str
    key: str
    size: int
    storage_class: str
    last_modified: datetime


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expiration_seconds: int = 3600
    http_method: str = "GET"


@dataclass
class PresignedUrlResponse:
    url: str
    expires_at: datetime
    bucket: str
    key: str
    http_method: str


@dataclass
class MetadataRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class MetadataResponse:
    bucket: str
    key: str
    content_type: Optional[str]
    content_length: int
    last_modified: datetime
    etag: Optional[str]
    version_id: Optional[str]
    storage_class: Optional[str]
    metadata: dict[str, str] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str
    delimiter: Optional[str] = None
    max_keys: int = 1000
    start_after: Optional[str] = None


@dataclass
class ObjectSummary:
    key: str
    size: int
    last_modified: datetime
    etag: Optional[str]
    storage_class: Optional[str]


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list[ObjectSummary] = field(default_factory=list)
    common_prefixes: list[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None


@dataclass
class OcrRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class OcrResponse:
    bucket: str
    key: str
    text: str
    confidence: float
    pages: int
    blocks: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class TranslateRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class TranslateResponse:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class SummaryRequest:
    text: str
    max_tokens: int = 500
    temperature: float = 0.3


@dataclass
class SummaryResponse:
    summary: str
    model_id: str
    input_tokens: int
    output_tokens: int


@dataclass
class EmbeddingRequest:
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class EmbeddingResponse:
    embedding: list[float]
    model_id: str
    input_tokens: int
    metadata: dict[str, str] = field(default_factory=dict)


def normalize_upload_response(
    raw: dict[str, Any], request: UploadRequest
) -> UploadResponse:
    return UploadResponse(
        etag=raw.get("ETag", "").strip('"'),
        version_id=raw.get("VersionId"),
        bucket=request.bucket,
        key=request.key,
        size=raw.get("ContentLength", 0),
        storage_class=raw.get("StorageClass", request.storage_class),
        last_modified=raw.get("LastModified", datetime.now(timezone.utc)),
    )


def normalize_metadata_response(
    raw: dict[str, Any], request: MetadataRequest
) -> MetadataResponse:
    custom_metadata = {}
    for k, v in raw.get("Metadata", {}).items():
        custom_metadata[k] = v

    return MetadataResponse(
        bucket=request.bucket,
        key=request.key,
        content_type=raw.get("ContentType"),
        content_length=raw.get("ContentLength", 0),
        last_modified=raw.get("LastModified", datetime.now(timezone.utc)),
        etag=raw.get("ETag", "").strip('"'),
        version_id=raw.get("VersionId"),
        storage_class=raw.get("StorageClass"),
        metadata=custom_metadata,
        server_side_encryption=raw.get("ServerSideEncryption"),
    )


def normalize_list_response(
    raw: dict[str, Any], request: ListPrefixRequest
) -> ListPrefixResponse:
    objects = []
    for item in raw.get("Contents", []):
        objects.append(
            ObjectSummary(
                key=item["Key"],
                size=item.get("Size", 0),
                last_modified=item.get("LastModified", datetime.now(timezone.utc)),
                etag=item.get("ETag", "").strip('"'),
                storage_class=item.get("StorageClass"),
            )
        )

    prefixes = [cp.get("Prefix", "") for cp in raw.get("CommonPrefixes", [])]

    return ListPrefixResponse(
        bucket=request.bucket,
        prefix=request.prefix,
        objects=objects,
        common_prefixes=prefixes,
        is_truncated=raw.get("IsTruncated", False),
        next_continuation_token=raw.get("NextContinuationToken"),
    )


def normalize_presigned_response(
    url: str, request: PresignedUrlRequest
) -> PresignedUrlResponse:
    from datetime import timedelta

    return PresignedUrlResponse(
        url=url,
        expires_at=datetime.now(timezone.utc)
        + timedelta(seconds=request.expiration_seconds),
        bucket=request.bucket,
        key=request.key,
        http_method=request.http_method,
    )


def normalize_ocr_response(raw: dict[str, Any], request: OcrRequest) -> OcrResponse:
    text_blocks = []
    full_text = []
    page_count = 0
    total_confidence = 0.0
    block_count = 0

    for block in raw.get("Blocks", []):
        block_type = block.get("BlockType", "")
        if block_type == "PAGE":
            page_count += 1
        if block_type in ("WORD", "LINE"):
            text = block.get("Text", "")
            confidence = block.get("Confidence", 0.0)
            full_text.append(text)
            total_confidence += confidence
            block_count += 1
            text_blocks.append(
                {
                    "type": block_type,
                    "text": text,
                    "confidence": confidence,
                    "geometry": block.get("Geometry", {}),
                }
            )

    avg_confidence = total_confidence / block_count if block_count > 0 else 0.0

    return OcrResponse(
        bucket=request.bucket,
        key=request.key,
        text="\n".join(full_text),
        confidence=avg_confidence,
        pages=max(page_count, 1),
        blocks=text_blocks,
    )


def normalize_translate_response(
    raw: dict[str, Any], request: TranslateRequest
) -> TranslateResponse:
    return TranslateResponse(
        translated_text=raw.get("TranslatedText", ""),
        source_language=raw.get("SourceLanguageCode", request.source_language),
        target_language=raw.get("TargetLanguageCode", request.target_language),
    )


def normalize_summary_response(raw: dict[str, Any], model_id: str) -> SummaryResponse:
    body = raw.get("body", {})
    if hasattr(body, "read"):
        import json

        body = json.loads(body.read().decode("utf-8"))

    content = body.get("content", [])
    summary_text = ""
    for item in content:
        if item.get("type") == "text":
            summary_text = item.get("text", "")
            break

    return SummaryResponse(
        summary=summary_text,
        model_id=model_id,
        input_tokens=body.get("usage", {}).get("input_tokens", 0),
        output_tokens=body.get("usage", {}).get("output_tokens", 0),
    )


def normalize_embedding_response(
    raw: dict[str, Any], model_id: str
) -> EmbeddingResponse:
    body = raw.get("body", {})
    if hasattr(body, "read"):
        import json

        body = json.loads(body.read().decode("utf-8"))

    return EmbeddingResponse(
        embedding=body.get("embedding", []),
        model_id=model_id,
        input_tokens=body.get("inputTextTokenCount", 0),
    )
