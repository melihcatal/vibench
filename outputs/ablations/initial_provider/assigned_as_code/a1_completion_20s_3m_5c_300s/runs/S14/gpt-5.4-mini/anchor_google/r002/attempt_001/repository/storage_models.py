def normalize_object_name(payload):
    if isinstance(payload, str):
        return payload
    return payload["object_name"]


def normalize_prefix(payload):
    if isinstance(payload, str):
        return payload
    return payload.get("prefix", "")


def to_object_response(blob):
    return {
        "object_name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "etag": blob.etag,
        "crc32c": blob.crc32c,
        "md5_hash": blob.md5_hash,
        "generation": blob.generation,
    }
