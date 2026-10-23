"""
storage_models.py - Define local request, response, and normalization helpers
for Managed Object Storage integration with Amazon S3.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class StorageUploadRequest:
    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"
    acl: str = "private"

    def __post_init__(self):
        if not self.file_path and not self.data:
            raise ValueError("Either file_path or data must be provided")


@dataclass
class StorageUploadResponse:
    success: bool
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    error: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expiration_seconds: int = 3600
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    url: str
    bucket: str
    key: str
    expires_at: datetime
    http_method: str = "GET"


@dataclass
class ObjectMetadataRequest:
    bucket: str
    key: str


@dataclass
class ObjectMetadataResponse:
    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None
    server_side_encryption: Optional[str] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: int = 1000


@dataclass
class StorageObjectInfo:
    key: str
    size: int
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: str = "STANDARD"


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: List[StorageObjectInfo] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None


@dataclass
class OcrRequest:
    bucket: str
    key: str
    document_type: str = "ANALYSIS"  # ANALYSIS or DETECTION


@dataclass
class OcrResponse:
    bucket: str
    key: str
    text: str = ""
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    pages: List[Dict[str, Any]] = field(default_factory=list)
    pages_count: int = 0
    confidence_score: float = 0.0


@dataclass
class TranslateRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"
    terminology_name: Optional[str] = None


@dataclass
class TranslateResponse:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class SummaryRequest:
    text: str
    bucket: Optional[str] = None
    key: Optional[str] = None
    max_tokens: int = 512
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"


@dataclass
class SummaryResponse:
    summary: str
    model_id: str
    tokens_used: int = 0
    bucket: Optional[str] = None
    key: Optional[str] = None


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model_id: str = "amazon.titan-embed-text-v2:0"


@dataclass
class EmbeddingObject:
    index: int
    embedding: List[float]
    text: str


@dataclass
class EmbeddingResponse:
    model_id: str
    embeddings: List[EmbeddingObject] = field(default_factory=list)
    input_token_count: int = 0


def normalize_s3_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize S3 SDK response into consistent dictionary format."""
    normalized = {}
    for key, value in response.items():
        if isinstance(value, datetime):
            normalized[key] = value
        elif hasattr(value, "isoformat"):
            normalized[key] = value.isoformat()
        else:
            normalized[key] = value
    return normalized


def build_s3_metadata(custom_metadata: Dict[str, str]) -> Dict[str, str]:
    """Build S3-compatible metadata dictionary with normalization."""
    return {
        k.lower().replace("_", "-"): str(v)
        for k, v in custom_metadata.items()
    }


def parse_s3_object_listing(listing: Dict[str, Any]) -> List[StorageObjectInfo]:
    """Parse S3 list_objects_v2 Contents into StorageObjectInfo list."""
    objects = []
    for item in listing.get("Contents", []):
        obj = StorageObjectInfo(
            key=item["Key"],
            size=item.get("Size", 0),
            last_modified=item.get("LastModified"),
            etag=item.get("ETag", "").strip('"'),
            storage_class=item.get("StorageClass", "STANDARD"),
        )
        objects.append(obj)
    return objects


def parse_textract_response(textract_output: Dict[str, Any]) -> Dict[str, Any]:
    """Parse Amazon Textract response into normalized text and blocks."""
    text_parts = []
    blocks = []
    pages = []
    current_page = []

    for block in textract_output.get("Blocks", []):
        block_info = {
            "id": block.get("Id"),
            "type": block.get("BlockType"),
            "confidence": block.get("Confidence", 0.0),
        }
        blocks.append(block_info)

        if block.get("BlockType") == "LINE":
            text_parts.append(block.get("Text", ""))
        elif block.get("BlockType") == "PAGE":
            if current_page:
                pages.append({"page_num": len(pages), "text": " ".join(current_page)})
            current_page = []

    if current_page:
        pages.append({"page_num": len(pages), "text": " ".join(current_page)})

    return {
        "text": "\n".join(text_parts),
        "blocks": blocks,
        "pages": pages,
    }
