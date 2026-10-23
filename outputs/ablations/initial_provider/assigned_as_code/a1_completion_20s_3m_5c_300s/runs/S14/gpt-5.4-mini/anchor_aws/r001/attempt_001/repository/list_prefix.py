from storage_client import get_s3_client


def list_prefix(payload, config=None):
    client, cfg = get_s3_client(config)
    prefix = payload.get("prefix", cfg.get("prefix", ""))
    response = client.list_objects_v2(Bucket=cfg["bucket"], Prefix=prefix)
    objects = []
    for item in response.get("Contents", []):
        objects.append({
            "object_name": item.get("Key"),
            "size": item.get("Size"),
            "last_modified": item.get("LastModified"),
            "etag": item.get("ETag"),
        })
    return {"prefix": prefix, "objects": objects, "is_truncated": response.get("IsTruncated", False)}
