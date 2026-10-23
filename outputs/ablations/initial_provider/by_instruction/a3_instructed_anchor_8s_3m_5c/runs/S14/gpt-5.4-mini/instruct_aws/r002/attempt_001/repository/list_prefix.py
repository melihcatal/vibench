from storage_client import default_bucket, s3_client
from storage_models import response_payload


def list_prefix(bucket=None, prefix="", delimiter=None, max_keys=1000):
    bucket_name = default_bucket(bucket)
    params = {"Bucket": bucket_name, "Prefix": prefix, "MaxKeys": int(max_keys)}
    if delimiter:
        params["Delimiter"] = delimiter
    result = s3_client().list_objects_v2(**params)
    items = []
    for entry in result.get("Contents", []):
        items.append({
            "key": entry.get("Key"),
            "last_modified": entry.get("LastModified"),
            "etag": entry.get("ETag"),
            "size": entry.get("Size"),
            "storage_class": entry.get("StorageClass"),
        })
    return response_payload(provider="aws", service="s3", bucket=bucket_name, prefix=prefix, objects=items, key_count=result.get("KeyCount"), is_truncated=result.get("IsTruncated"))
