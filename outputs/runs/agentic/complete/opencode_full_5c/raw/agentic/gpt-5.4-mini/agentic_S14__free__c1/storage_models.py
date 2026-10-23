from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _clean_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


@dataclass
class ObjectUploadRequest:
    bucket: str
    key: str
    body: Any
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def normalize(self) -> "ObjectUploadRequest":
        return ObjectUploadRequest(
            _clean_str(self.bucket) or "",
            _clean_str(self.key) or "",
            self.body,
            _clean_str(self.content_type),
            _clean_dict(self.metadata),
        )


@dataclass
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 900

    def normalize(self) -> "PresignedDownloadRequest":
        return PresignedDownloadRequest(
            _clean_str(self.bucket) or "",
            _clean_str(self.key) or "",
            int(self.expires_in or 900),
        )


@dataclass
class ObjectMetadataRequest:
    bucket: str
    key: str

    def normalize(self) -> "ObjectMetadataRequest":
        return ObjectMetadataRequest(
            _clean_str(self.bucket) or "", _clean_str(self.key) or ""
        )


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    max_items: Optional[int] = None

    def normalize(self) -> "ListPrefixRequest":
        return ListPrefixRequest(
            _clean_str(self.bucket) or "",
            _clean_str(self.prefix) or "",
            self.max_items if self.max_items is None else int(self.max_items),
        )


def normalize_object_result(data: Any) -> Dict[str, Any]:
    payload = _clean_dict(data)
    return {
        "bucket": _clean_str(payload.get("bucket")),
        "key": _clean_str(payload.get("key")),
        "etag": _clean_str(payload.get("etag")),
        "version_id": _clean_str(payload.get("version_id")),
        "content_type": _clean_str(payload.get("content_type")),
        "content_length": payload.get("content_length"),
        "metadata": _clean_dict(payload.get("metadata")),
        "raw": payload,
    }


def normalize_list_result(data: Any) -> Dict[str, Any]:
    payload = _clean_dict(data)
    return {
        "bucket": _clean_str(payload.get("bucket")),
        "prefix": _clean_str(payload.get("prefix")),
        "objects": _clean_list(payload.get("objects")),
        "next_token": _clean_str(payload.get("next_token")),
        "raw": payload,
    }
