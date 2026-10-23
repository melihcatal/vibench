from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


def normalize_etag(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value).strip('"')


def normalize_metadata(value: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(value)
    if "ETag" in result:
        result["ETag"] = normalize_etag(result["ETag"])
    if "LastModified" in result and isinstance(result["LastModified"], datetime):
        result["LastModified"] = result["LastModified"].isoformat()
    return result


def normalize_list_objects_v2(value: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(value)
    contents = []
    for item in result.get("Contents", []) or []:
        normalized = dict(item)
        if "LastModified" in normalized and isinstance(normalized["LastModified"], datetime):
            normalized["LastModified"] = normalized["LastModified"].isoformat()
        if "ETag" in normalized:
            normalized["ETag"] = normalize_etag(normalized["ETag"])
        contents.append(normalized)
    result["Contents"] = contents
    return result


@dataclass
class UploadObjectRequest:
    bucket: Optional[str]
    key: str
    data: Any
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None


@dataclass
class UploadObjectResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket: Optional[str]
    key: str
    expires_in_seconds: int = 3600
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedDownloadResponse:
    bucket: str
    key: str
    url: str
    expires_in_seconds: int


@dataclass
class ObjectMetadataResponse:
    bucket: str
    key: str
    metadata: Dict[str, Any]

    @classmethod
    def from_head_object(cls, bucket: str, key: str, metadata: Dict[str, Any]) -> "ObjectMetadataResponse":
        return cls(bucket=bucket, key=key, metadata=metadata)


@dataclass
class ObjectSummary:
    key: str
    size: int
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None

    @classmethod
    def from_s3(cls, item: Dict[str, Any]) -> "ObjectSummary":
        return cls(key=str(item.get("Key", "")), size=int(item.get("Size", 0)), last_modified=item.get("LastModified"), etag=normalize_etag(item.get("ETag")), storage_class=item.get("StorageClass"))


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: List[ObjectSummary]
    is_truncated: bool
    key_count: int


@dataclass
class StoredDocumentOcrResult:
    bucket: str
    key: str
    text: str
    language_code: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class StoredTextTranslateResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str


@dataclass
class StoredAssetSummaryResult:
    bucket: str
    key: str
    summary: str
    content_type: Optional[str] = None


@dataclass
class AssetMetadataEmbeddingResult:
    bucket: str
    key: str
    embedding: List[float]
    dimensions: int
