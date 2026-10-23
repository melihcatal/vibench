from pydantic import BaseModel
from typing import Optional, BinaryIO, List, Dict
from datetime import timedelta, datetime

class UploadRequest(BaseModel):
    bucket_name: str
    object_key: str
    content: BinaryIO | bytes | str
    content_type: Optional[str] = None

class UploadResponse(BaseModel):
    bucket_name: str
    object_key: str
    public_url: Optional[str]
    size: Optional[int]
    etag: Optional[str]

class PresignedDownloadRequest(BaseModel):
    bucket_name: str
    object_key: str
    expiration: Optional[timedelta] = None

class PresignedDownloadResponse(BaseModel):
    bucket_name: str
    object_key: str
    presigned_url: str
    expires_at: Optional[timedelta]

class ObjectMetadataRequest(BaseModel):
    bucket_name: str
    object_key: str

class ObjectMetadataResponse(BaseModel):
    bucket_name: str
    object_key: str
    content_type: Optional[str]
    size: Optional[int]
    etag: Optional[str]
    last_modified: Optional[datetime]
    metadata: Dict[str, str]

class ListedObject(BaseModel):
    object_key: str
    size: Optional[int]
    last_modified: Optional[datetime]
    etag: Optional[str]

class ListPrefixRequest(BaseModel):
    bucket_name: str
    prefix: str
    delimiter: Optional[str] = None

class ListPrefixResponse(BaseModel):
    bucket_name: str
    prefix: str
    objects: List[ListedObject]