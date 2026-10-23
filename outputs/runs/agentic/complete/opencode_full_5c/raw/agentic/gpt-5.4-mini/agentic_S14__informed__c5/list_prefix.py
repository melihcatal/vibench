from storage_client import get_bucket_name, get_s3_client
from storage_models import ListedObject


def list_prefix(bucket=None, prefix="", max_keys=1000):
    client = get_s3_client()
    response = client.list_objects_v2(
        Bucket=get_bucket_name(bucket), Prefix=prefix, MaxKeys=max_keys
    )
    items = []
    for obj in response.get("Contents", []):
        items.append(
            ListedObject(
                bucket=get_bucket_name(bucket),
                key=obj.get("Key"),
                size=obj.get("Size"),
                last_modified=obj.get("LastModified"),
                etag=obj.get("ETag"),
            )
        )
    return items
