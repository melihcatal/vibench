def normalize_object_name(value):
    return str(value).lstrip("/")


def normalize_prefix(value):
    if value in (None, ""):
        return ""
    return str(value).lstrip("/")


def metadata_from_head_response(head_response):
    return {
        "object_name": head_response.get("Key"),
        "content_length": head_response.get("ContentLength"),
        "content_type": head_response.get("ContentType"),
        "etag": head_response.get("ETag"),
        "last_modified": head_response.get("LastModified"),
        "metadata": head_response.get("Metadata", {}),
    }
