from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class UploadRequest:
    bucket_name: str
    object_key: str
    body: bytes
    content_type: str = "application/octet-stream"
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    object_id: str
    etag: str
    version_id: Optional[str] = None
    provider: str = "aws_s3"


@dataclass
class PresignedDownloadResponse:
    download_url: str
    expires_at: datetime
    provider: str = "aws_s3"


@dataclass
class ObjectMetadataResponse:
    object_id: str
    metadata: Dict[str, str]
    provider: str = "aws_s3"


@dataclass
class ListedObject:
    object_id: str
    size: int
    last_modified: datetime
    etag: str


@dataclass
class ListPrefixResponse:
    bucket_name: str
    prefix: str
    objects: List[ListedObject]
    provider: str = "aws_s3"
