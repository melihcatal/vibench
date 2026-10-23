from dataclasses import dataclass
from typing import Optional


@dataclass
class UploadRequest:
    bucket_name: str
    object_key: str
    file_path: Optional[str] = None
    byte_stream: Optional[bytes] = None


@dataclass
class DownloadResponse:
    url: str
    expires_at: datetime.datetime


@dataclass
class MetadataResponse:
    metadata: dict


@dataclass
class ListResponse:
    object_keys: list[str]
