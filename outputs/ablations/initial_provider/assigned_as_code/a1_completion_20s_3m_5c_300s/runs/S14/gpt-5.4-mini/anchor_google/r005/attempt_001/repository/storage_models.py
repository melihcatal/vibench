def normalize_object_name(value):
    if value is None:
        return ""
    return str(value).lstrip("/")


def normalize_metadata(blob):
    return {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "md5_hash": blob.md5_hash,
        "crc32c": blob.crc32c,
        "metadata": dict(blob.metadata or {}),
    }


def normalize_listing(iterator):
    return [normalize_metadata(blob) for blob in iterator]
