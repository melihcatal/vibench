from storage_client import create_s3_client, resolve_bucket
from storage_models import ListPrefixRequest, normalize_list_result


def list_prefix(bucket: str, prefix: str = "", max_items=None):
    request = ListPrefixRequest(
        bucket=bucket, prefix=prefix, max_items=max_items
    ).normalize()
    s3 = create_s3_client()
    kwargs = {"Bucket": resolve_bucket(request.bucket), "Prefix": request.prefix}
    if request.max_items is not None:
        kwargs["MaxKeys"] = request.max_items
    response = s3.list_objects_v2(**kwargs)
    objects = []
    for item in response.get("Contents", []):
        objects.append(
            {
                "key": item.get("Key"),
                "size": item.get("Size"),
                "last_modified": item.get("LastModified").isoformat()
                if item.get("LastModified")
                else None,
                "etag": item.get("ETag"),
            }
        )
    return normalize_list_result(
        {
            "bucket": kwargs["Bucket"],
            "prefix": request.prefix,
            "objects": objects,
            "next_token": response.get("NextContinuationToken"),
        }
    )
