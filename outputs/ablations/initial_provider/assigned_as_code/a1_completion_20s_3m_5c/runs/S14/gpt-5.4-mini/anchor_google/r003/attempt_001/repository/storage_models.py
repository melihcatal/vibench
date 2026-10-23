def normalize_payload(payload):
    payload = dict(payload or {})
    if "data" in payload and isinstance(payload["data"], str):
        payload["data"] = payload["data"].encode("utf-8")
    return payload


def normalize_object_name(payload):
    return (payload or {}).get("object_name") or (payload or {}).get("name")


def metadata_response(blob):
    return {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "content_language": blob.content_language,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "md5_hash": blob.md5_hash,
        "crc32c": blob.crc32c,
        "etag": blob.etag,
        "generation": blob.generation,
    }


def object_listing(items):
    return [{"name": item.name, "bucket": item.bucket.name, "size": item.size, "updated": item.updated.isoformat() if item.updated else None} for item in items]
