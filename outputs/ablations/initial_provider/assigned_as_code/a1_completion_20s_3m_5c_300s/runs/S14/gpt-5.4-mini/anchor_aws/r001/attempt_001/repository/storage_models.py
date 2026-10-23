import base64


def normalize_config(config=None):
    config = config or {}
    return {
        "region": config.get("region"),
        "bucket": config.get("bucket"),
        "prefix": config.get("prefix", ""),
        "expires_in": int(config.get("expires_in", 3600)),
        "output_format": config.get("output_format", "text"),
        "language": config.get("language", "en"),
        "provider_region": config.get("provider_region") or config.get("region"),
    }


def normalize_object_name(payload):
    return payload.get("object_name") or payload.get("key") or payload.get("name")


def normalize_bytes(data):
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, memoryview):
        return data.tobytes()
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, dict) and data.get("base64"):
        return base64.b64decode(data["base64"])
    return bytes(data)


def metadata_view(head_response):
    return {
        "etag": head_response.get("ETag"),
        "content_length": head_response.get("ContentLength"),
        "content_type": head_response.get("ContentType"),
        "last_modified": head_response.get("LastModified"),
        "storage_class": head_response.get("StorageClass"),
        "metadata": head_response.get("Metadata", {}),
    }
