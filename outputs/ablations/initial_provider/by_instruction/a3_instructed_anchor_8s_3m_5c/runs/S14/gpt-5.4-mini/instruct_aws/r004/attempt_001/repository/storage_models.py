from dataclasses import dataclass


def _to_dict_headers(metadata):
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items()}


@dataclass
class UploadObjectRequest:
    bucket: str
    key: str
    body: object
    content_type: str = None
    metadata: dict = None


@dataclass
class UploadObjectResponse:
    bucket: str
    key: str
    etag: str = None
    version_id: str = None


@dataclass
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600


@dataclass
class ObjectMetadataResponse:
    bucket: str
    key: str
    etag: str = None
    content_length: int = None
    content_type: str = None
    last_modified: object = None
    metadata: dict = None


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list
    is_truncated: bool = False
    next_token: str = None


def normalize_object_metadata(bucket, key, head_response):
    return ObjectMetadataResponse(
        bucket=bucket,
        key=key,
        etag=head_response.get("ETag"),
        content_length=head_response.get("ContentLength"),
        content_type=head_response.get("ContentType"),
        last_modified=head_response.get("LastModified"),
        metadata=_to_dict_headers(head_response.get("Metadata")),
    )
