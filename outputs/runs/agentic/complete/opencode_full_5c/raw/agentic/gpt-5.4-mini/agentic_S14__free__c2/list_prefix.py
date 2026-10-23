from storage_client import storage_client
from storage_models import ListObjectsResponse


def list_prefix(bucket: str, prefix: str = "") -> ListObjectsResponse:
    client = storage_client("s3")
    result = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    objects = []
    for item in result.get("Contents", []):
        objects.append(
            {
                "key": item.get("Key"),
                "size": item.get("Size"),
                "last_modified": str(item.get("LastModified"))
                if item.get("LastModified")
                else None,
                "etag": item.get("ETag"),
            }
        )
    return ListObjectsResponse(
        bucket=bucket, prefix=prefix, objects=objects, raw=result
    )
