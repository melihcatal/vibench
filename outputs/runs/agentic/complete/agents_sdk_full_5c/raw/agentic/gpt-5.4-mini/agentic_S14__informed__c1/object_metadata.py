from typing import Optional

from storage_client import get_bucket
from storage_models import MetadataResult


def read_object_metadata(object_name: str, bucket_name: Optional[str] = None) -> MetadataResult:
    bucket = get_bucket(bucket_name)
    blob = bucket.get_blob(object_name)
    if blob is None:
        raise FileNotFoundError(object_name)
    return MetadataResult(
        bucket_name=bucket.name,
        object_name=blob.name,
        content_type=blob.content_type,
        content_length=blob.size,
        md5_hash=blob.md5_hash,
        generation=str(blob.generation) if blob.generation is not None else None,
        updated=str(blob.updated) if blob.updated is not None else None,
        metadata=dict(blob.metadata or {}),
    )
