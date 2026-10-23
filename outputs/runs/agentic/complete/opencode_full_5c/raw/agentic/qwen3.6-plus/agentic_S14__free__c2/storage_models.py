import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


@dataclass
class UploadRequest:
    bucket: str
    key: str
    content_type: str = "application/octet-stream"
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class UploadResponse:
    bucket: str
    key: str
    etag: str
    version_id: Optional[str] = None
    storage_class: str = "STANDARD"
    size_bytes: int = 0
    last_modified: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expiration_seconds: int = 3600
    http_method: str = "GET"
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    url: str
    bucket: str
    key: str
    expires_at: str
    http_method: str = "GET"


@dataclass
class MetadataRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    content_type: str = ""
    content_length: int = 0
    etag: str = ""
    last_modified: str = ""
    storage_class: str = ""
    version_id: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    delete_marker: bool = False


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: int = 1000
    start_after: str = ""


@dataclass
class ListedObject:
    key: str
    size: int = 0
    etag: str = ""
    last_modified: str = ""
    storage_class: str = ""


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: List[ListedObject] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    key_count: int = 0


@dataclass
class OcrRequest:
    bucket: str
    key: str
    feature_types: List[str] = field(default_factory=lambda: ["TABLES", "FORMS"])


@dataclass
class OcrResponse:
    bucket: str
    key: str
    text: str = ""
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    pages: int = 0
    confidence: float = 0.0


@dataclass
class TranslateRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"
    terminology_names: Optional[List[str]] = None


@dataclass
class TranslateResponse:
    translated_text: str
    source_language: str = ""
    target_language: str = "en"


@dataclass
class SummaryRequest:
    text: str
    max_tokens: int = 300
    temperature: float = 0.3
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"


@dataclass
class SummaryResponse:
    summary: str
    model_id: str = ""
    token_usage: Dict[str, int] = field(default_factory=dict)


@dataclass
class EmbeddingRequest:
    text: str
    model_id: str = "amazon.titan-embed-text-v2:0"
    dimensions: int = 1024
    normalize: bool = True


@dataclass
class EmbeddingResponse:
    embedding: List[float] = field(default_factory=list)
    model_id: str = ""
    input_tokens: int = 0


def normalize_upload_response(
    s3_response: Dict[str, Any], bucket: str, key: str, size_bytes: int
) -> UploadResponse:
    return UploadResponse(
        bucket=bucket,
        key=key,
        etag=s3_response.get("ETag", "").strip('"'),
        version_id=s3_response.get("VersionId"),
        storage_class=s3_response.get("StorageClass", "STANDARD"),
        size_bytes=size_bytes,
        last_modified=s3_response.get("LastModified", "").isoformat()
        if s3_response.get("LastModified")
        else None,
    )


def normalize_object_metadata(
    head_response: Dict[str, Any], bucket: str, key: str
) -> ObjectMetadata:
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        content_type=head_response.get("ContentType", ""),
        content_length=head_response.get("ContentLength", 0),
        etag=head_response.get("ETag", "").strip('"'),
        last_modified=head_response.get("LastModified", "").isoformat()
        if head_response.get("LastModified")
        else "",
        storage_class=head_response.get("StorageClass", ""),
        version_id=head_response.get("VersionId"),
        metadata={
            k.replace("x-amz-meta-", ""): v
            for k, v in head_response.get("Metadata", {}).items()
        },
        delete_marker=head_response.get("DeleteMarker", False),
    )


def normalize_list_response(
    list_response: Dict[str, Any], bucket: str, prefix: str
) -> ListPrefixResponse:
    objects = [
        ListedObject(
            key=obj["Key"],
            size=obj.get("Size", 0),
            etag=obj.get("ETag", "").strip('"'),
            last_modified=obj.get("LastModified", "").isoformat()
            if obj.get("LastModified")
            else "",
            storage_class=obj.get("StorageClass", ""),
        )
        for obj in list_response.get("Contents", [])
    ]
    common_prefixes = [cp["Prefix"] for cp in list_response.get("CommonPrefixes", [])]
    return ListPrefixResponse(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        common_prefixes=common_prefixes,
        is_truncated=list_response.get("IsTruncated", False),
        next_continuation_token=list_response.get("NextContinuationToken"),
        key_count=list_response.get("KeyCount", len(objects)),
    )


def normalize_ocr_response(
    textract_response: Dict[str, Any], bucket: str, key: str
) -> OcrResponse:
    blocks = textract_response.get("Blocks", [])
    text_parts = []
    total_confidence = 0.0
    confidence_count = 0
    page_count = 0
    for block in blocks:
        if block.get("BlockType") == "PAGE":
            page_count += 1
        if block.get("BlockType") == "LINE":
            text_parts.append(block.get("Text", ""))
            conf = block.get("Confidence", 0)
            total_confidence += conf
            confidence_count += 1
    avg_confidence = (
        total_confidence / confidence_count if confidence_count > 0 else 0.0
    )
    return OcrResponse(
        bucket=bucket,
        key=key,
        text="\n".join(text_parts),
        blocks=blocks,
        pages=max(page_count, 1),
        confidence=round(avg_confidence, 2),
    )
