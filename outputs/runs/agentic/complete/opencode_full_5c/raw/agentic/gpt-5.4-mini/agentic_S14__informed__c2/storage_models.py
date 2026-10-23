from dataclasses import dataclass
from io import BytesIO
from mimetypes import guess_type
from typing import Any, Dict, Iterable, Optional, Union


BodyType = Union[str, bytes, bytearray, BytesIO]


def normalize_body(body: BodyType) -> Union[str, bytes]:
    if isinstance(body, BytesIO):
        return body.getvalue()
    if isinstance(body, bytearray):
        return bytes(body)
    return body


def infer_content_type(key: str, fallback: str = 'application/octet-stream') -> str:
    content_type, _ = guess_type(key)
    return content_type or fallback


def object_key_from_input(source: Union[str, bytes, bytearray, BytesIO], key: Optional[str] = None) -> str:
    if key:
        return key
    if isinstance(source, str):
        return source.rsplit('/', 1)[-1]
    return 'object.bin'


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: BodyType
    content_type: str

    @classmethod
    def from_source(cls, source: Union[str, bytes, bytearray, BytesIO], bucket: Optional[str] = None, key: Optional[str] = None, content_type: Optional[str] = None):
        resolved_bucket = bucket or ''
        resolved_key = object_key_from_input(source, key=key)
        resolved_content_type = content_type or infer_content_type(resolved_key)
        body = source if not isinstance(source, str) or source.startswith('s3://') else source.encode('utf-8')
        return cls(bucket=resolved_bucket, key=resolved_key, body=body, content_type=resolved_content_type)


@dataclass
class UploadResult:
    bucket: str
    key: str
    content_type: str


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expires_in: int


@dataclass
class PresignedUrlResult:
    bucket: str
    key: str
    url: str
    expires_in: int


@dataclass
class MetadataResult:
    bucket: str
    key: str
    metadata: Dict[str, Any]

    @classmethod
    def from_head(cls, bucket: str, key: str, head: Dict[str, Any]):
        return cls(bucket=bucket, key=key, metadata=head)


@dataclass
class ListPrefixResult:
    bucket: str
    prefix: str
    keys: list

    @classmethod
    def from_list_response(cls, bucket: str, prefix: str, response: Dict[str, Any]):
        contents = response.get('Contents', []) or []
        keys = [item.get('Key') for item in contents if item.get('Key')]
        return cls(bucket=bucket, prefix=prefix, keys=keys)
