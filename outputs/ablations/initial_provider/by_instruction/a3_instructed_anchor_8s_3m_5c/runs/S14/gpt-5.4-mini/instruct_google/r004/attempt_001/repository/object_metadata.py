from google.cloud import storage

from storage_client import get_bucket
from storage_models import ObjectMetadata, normalize_object_name


def object_metadata(bucket_name: str, object_name: str) -> dict:
    bucket = get_bucket(bucket_name)
    blob = bucket.get_blob(normalize_object_name(object_name))
    if blob is None:
        raise FileNotFoundError(object_name)
    blob.reload()
    return ObjectMetadata(
        bucket=bucket_name,
        name=blob.name,
        size=blob.size,
        content_type=blob.content_type,
        md5_hash=blob.md5_hash,
        crc32c=blob.crc32c,
        updated=blob.updated.isoformat() if blob.updated else None,
        etag=blob.etag,
        generation=blob.generation,
        metadata=dict(blob.metadata or {}),
    ).to_dict()
