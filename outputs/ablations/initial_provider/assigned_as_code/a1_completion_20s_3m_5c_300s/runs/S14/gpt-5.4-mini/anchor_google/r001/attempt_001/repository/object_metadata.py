from storage_client import get_blob
from storage_models import normalize_metadata, normalize_object_name


def object_metadata(payload, config=None):
    blob, _ = get_blob(normalize_object_name(payload), config)
    blob.reload()
    return normalize_metadata({
        "object_name": payload["object_name"],
        "bucket": blob.bucket.name,
        "content_type": blob.content_type,
        "size": blob.size,
        "updated": blob.updated,
        "created": getattr(blob, "time_created", None),
        "md5_hash": blob.md5_hash,
        "crc32c": blob.crc32c,
        "etag": blob.etag,
    })
