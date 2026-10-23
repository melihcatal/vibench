from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Union


BodyType = Union[bytes, bytearray, memoryview, str, Path, BytesIO]


@dataclass(frozen=True)
class UploadRequest:
    bucket: str
    key: str
    body: BodyType
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class UploadResponse:
    bucket: str
    key: str
    size: int
    etag: Optional[str]


@dataclass(frozen=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in_seconds: Optional[int] = None


@dataclass(frozen=True)
class PresignedDownloadResponse:
    url: str
    expires_in_seconds: int


@dataclass(frozen=True)
class ObjectMetadataRequest:
    bucket: str
    key: str


@dataclass(frozen=True)
class ObjectMetadataResponse:
    bucket: str
    key: str
    size: int
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str]


@dataclass(frozen=True)
class ListPrefixRequest:
    bucket: str
    prefix: Optional[str] = None


@dataclass(frozen=True)
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list


def coerce_body_bytes(body: BodyType) -> bytes:
    if isinstance(body, bytes):
        return body
    if isinstance(body, bytearray):
        return bytes(body)
    if isinstance(body, memoryview):
        return body.tobytes()
    if isinstance(body, str):
        path = Path(body)
        return path.read_bytes() if path.exists() else body.encode("utf-8")
    if isinstance(body, Path):
        return body.read_bytes()
    if isinstance(body, BytesIO):
        return body.getvalue()
    raise TypeError(f"Unsupported body type: {type(body)!r}")


def normalize_metadata_response(bucket: str, key: str, head: Mapping[str, Any]) -> ObjectMetadataResponse:
    return ObjectMetadataResponse(
        bucket=bucket,
        key=key,
        size=int(head.get("ContentLength", 0)),
        content_type=head.get("ContentType"),
        etag=head.get("ETag"),
        last_modified=str(head.get("LastModified")) if head.get("LastModified") is not None else None,
        metadata=dict(head.get("Metadata") or {}),
    )


def normalize_list_response(bucket: str, prefix: str, pages: Iterable[Mapping[str, Any]]) -> ListPrefixResponse:
    objects = []
    for page in pages:
        for item in page.get("Contents", []) or []:
            objects.append(
                {
                    "key": item.get("Key"),
                    "size": int(item.get("Size", 0)),
                    "etag": item.get("ETag"),
                    "last_modified": str(item.get("LastModified")) if item.get("LastModified") is not None else None,
                }
            )
    return ListPrefixResponse(bucket=bucket, prefix=prefix, objects=objects)
