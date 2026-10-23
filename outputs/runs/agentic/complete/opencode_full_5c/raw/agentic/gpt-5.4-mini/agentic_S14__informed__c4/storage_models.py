from dataclasses import asdict, dataclass


@dataclass
class ObjectUploadRequest:
    bucket: str
    key: str
    body: bytes
    content_type: str | None = None


@dataclass
class ObjectResult:
    bucket: str
    key: str
    etag: str | None = None
    version_id: str | None = None


def normalize_metadata(metadata: dict | None) -> dict:
    return {str(k): str(v) for k, v in (metadata or {}).items()}


def to_dict(obj):
    return asdict(obj)
