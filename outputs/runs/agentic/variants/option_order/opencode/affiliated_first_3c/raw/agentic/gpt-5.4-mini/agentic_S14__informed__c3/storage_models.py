from dataclasses import dataclass
from typing import Any, Iterable


def normalize_body(body: Any) -> Any:
    if isinstance(body, str):
        return body.encode("utf-8")
    if isinstance(body, bytearray):
        return bytes(body)
    return body


def normalize_metadata(metadata: dict | None) -> dict:
    return {str(k): "" if v is None else str(v) for k, v in (metadata or {}).items()}


def normalize_object_location(bucket: str, key: str) -> dict:
    return {"bucket": bucket, "key": key, "uri": f"s3://{bucket}/{key}"}


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: Any
    content_type: str | None = None
    metadata: dict | None = None
    acl: str | None = None


@dataclass
class UploadResponse:
    bucket: str
    key: str
    uri: str


@dataclass
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600


@dataclass
class PresignedDownloadResponse:
    url: str
    bucket: str
    key: str
    expires_in: int


@dataclass
class HeadObjectRequest:
    bucket: str
    key: str


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    etag: str | None = None
    content_length: int | None = None
    content_type: str | None = None
    last_modified: Any | None = None
    metadata: dict | None = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: str | None = None
    max_keys: int | None = None


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list
    common_prefixes: list
    is_truncated: bool
    next_continuation_token: str | None = None


def normalize_head_object(response: dict, bucket: str, key: str) -> dict:
    return {
        "bucket": bucket,
        "key": key,
        "etag": response.get("ETag"),
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "last_modified": response.get("LastModified"),
        "metadata": response.get("Metadata", {}),
    }


def normalize_list_objects(response: dict, bucket: str, prefix: str) -> dict:
    objects = []
    for item in response.get("Contents", []) or []:
        objects.append({
            "key": item.get("Key"),
            "size": item.get("Size"),
            "etag": item.get("ETag"),
            "last_modified": item.get("LastModified"),
            "storage_class": item.get("StorageClass"),
        })
    return {
        "bucket": bucket,
        "prefix": prefix,
        "objects": objects,
        "common_prefixes": [p.get("Prefix") for p in response.get("CommonPrefixes", []) or []],
        "is_truncated": bool(response.get("IsTruncated")),
        "next_continuation_token": response.get("NextContinuationToken"),
    }
