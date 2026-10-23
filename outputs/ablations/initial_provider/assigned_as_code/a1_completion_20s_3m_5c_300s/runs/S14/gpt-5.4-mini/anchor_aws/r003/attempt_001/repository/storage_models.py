def normalize_key(name, prefix=""):
    prefix = prefix or ""
    if prefix and not prefix.endswith("/"):
        prefix = prefix + "/"
    return f"{prefix}{name}" if name else prefix.rstrip("/")


def normalize_listing(contents):
    items = []
    for item in contents or []:
        items.append({
            "object_name": item.get("Key"),
            "size": item.get("Size"),
            "etag": item.get("ETag"),
            "last_modified": item.get("LastModified"),
        })
    return items


def normalize_metadata(head):
    return {
        "object_name": head.get("Key"),
        "content_length": head.get("ContentLength"),
        "content_type": head.get("ContentType"),
        "etag": head.get("ETag"),
        "last_modified": head.get("LastModified"),
        "metadata": head.get("Metadata", {}),
    }
