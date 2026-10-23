import hashlib
import mimetypes
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class UploadRequest:
    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"
    server_side_encryption: Optional[str] = None
    tags: dict[str, str] = field(default_factory=dict)

    def resolve_content_type(self) -> str:
        if self.content_type:
            return self.content_type
        if self.file_path:
            guessed, _ = mimetypes.guess_type(self.file_path)
            if guessed:
                return guessed
        return "application/octet-stream"

    def compute_md5(self) -> Optional[str]:
        if self.data:
            return hashlib.md5(self.data).hexdigest()
        if self.file_path:
            with open(self.file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        return None


@dataclass
class UploadResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    content_length: int = 0
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    server_side_encryption: Optional[str] = None
    request_id: Optional[str] = None

    @classmethod
    def from_s3_response(
        cls, bucket: str, key: str, response: dict[str, Any]
    ) -> "UploadResponse":
        return cls(
            bucket=bucket,
            key=key,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            content_length=response.get("ContentLength", 0),
            content_type=response.get("ContentType"),
            last_modified=response.get("LastModified"),
            storage_class=response.get("StorageClass"),
            server_side_encryption=response.get("ServerSideEncryption"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: int = 0
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    server_side_encryption: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    delete_marker: bool = False
    expiration: Optional[str] = None
    restore: Optional[str] = None
    cache_control: Optional[str] = None
    content_disposition: Optional[str] = None
    content_encoding: Optional[str] = None
    content_language: Optional[str] = None
    website_redirect_location: Optional[str] = None

    @classmethod
    def from_s3_head(
        cls, bucket: str, key: str, head_response: dict[str, Any]
    ) -> "ObjectMetadata":
        return cls(
            bucket=bucket,
            key=key,
            content_type=head_response.get("ContentType"),
            content_length=head_response.get("ContentLength", 0),
            etag=head_response.get("ETag", "").strip('"'),
            last_modified=head_response.get("LastModified"),
            storage_class=head_response.get("StorageClass"),
            version_id=head_response.get("VersionId"),
            server_side_encryption=head_response.get("ServerSideEncryption"),
            metadata={
                k.replace("x-amz-meta-", ""): v
                for k, v in head_response.get("Metadata", {}).items()
            },
            delete_marker=head_response.get("DeleteMarker", False),
            expiration=head_response.get("Expiration"),
            restore=head_response.get("Restore"),
            cache_control=head_response.get("CacheControl"),
            content_disposition=head_response.get("ContentDisposition"),
            content_encoding=head_response.get("ContentEncoding"),
            content_language=head_response.get("ContentLanguage"),
            website_redirect_location=head_response.get("WebsiteRedirectLocation"),
        )


@dataclass
class ObjectSummary:
    bucket: str
    key: str
    size: int = 0
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    owner: Optional[dict[str, str]] = None

    @classmethod
    def from_s3_object(cls, bucket: str, obj: dict[str, Any]) -> "ObjectSummary":
        return cls(
            bucket=bucket,
            key=obj["Key"],
            size=obj.get("Size", 0),
            etag=obj.get("ETag", "").strip('"'),
            last_modified=obj.get("LastModified"),
            storage_class=obj.get("StorageClass"),
            owner=obj.get("Owner"),
        )


@dataclass
class PresignedUrlResponse:
    bucket: str
    key: str
    url: str
    expires_in: int
    http_method: str = "GET"
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def expires_at(self) -> datetime:
        return (
            self.generated_at.replace(second=self.generated_at.second + self.expires_in)
            if self.generated_at
            else datetime.now(timezone.utc)
        )


@dataclass
class ListObjectsResponse:
    bucket: str
    prefix: str
    objects: list[ObjectSummary] = field(default_factory=list)
    common_prefixes: list[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    key_count: int = 0
    max_keys: int = 1000
    delimiter: Optional[str] = None

    @classmethod
    def from_s3_list(
        cls,
        bucket: str,
        prefix: str,
        response: dict[str, Any],
        delimiter: Optional[str] = None,
    ) -> "ListObjectsResponse":
        objects = [
            ObjectSummary.from_s3_object(bucket, obj)
            for obj in response.get("Contents", [])
        ]
        common_prefixes = [cp["Prefix"] for cp in response.get("CommonPrefixes", [])]
        return cls(
            bucket=bucket,
            prefix=prefix,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=response.get("IsTruncated", False),
            next_continuation_token=response.get("NextContinuationToken"),
            key_count=response.get("KeyCount", len(objects)),
            max_keys=response.get("MaxKeys", 1000),
            delimiter=delimiter,
        )
