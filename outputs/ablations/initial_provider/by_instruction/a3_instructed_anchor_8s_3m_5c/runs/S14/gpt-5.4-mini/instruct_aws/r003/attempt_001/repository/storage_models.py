from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


@dataclass
class StorageObjectRequest:
    bucket: str
    key: str
    body: Optional[Union[bytes, str]] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class StorageObjectResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_body(body: Optional[Union[bytes, str]]) -> Optional[Union[bytes, str]]:
    if body is None or isinstance(body, (bytes, str)):
        return body
    return str(body)


def metadata_from_head(response: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in response.items() if k.lower().startswith("x-amz-") or k in {"ContentLength", "ContentType", "ETag", "LastModified", "VersionId", "AcceptRanges"}}
