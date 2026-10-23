# storage_models.py
# [HELPER] Request, response, and normalization helpers for Managed Object Storage

from dataclasses import dataclass, asdict
from datetime import datetime


class UploadResponse:
    """Response model for upload operations."""

    blob_name: str
    size: int
    updated: datetime

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class PresignedDownloadResponse:
    url: str
    expires_at: datetime

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class ObjectMetadataResponse:
    bucket: str
    blob: str
    content_type: str | None = None
    size: int | None = None
    created: datetime | None = None
    updated: datetime | None = None
    metadata: dict = dataclasses.field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list[dict]
    prefixes: list[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
