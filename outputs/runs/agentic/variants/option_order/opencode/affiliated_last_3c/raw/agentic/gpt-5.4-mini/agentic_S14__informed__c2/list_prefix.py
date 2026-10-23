import os

from storage_client import get_bucket_name, get_client
from storage_models import normalize_prefix


def list_prefix(bucket_name: str | None, prefix: str | None = None) -> list[dict]:
    client = get_client()
    bucket = client.bucket(get_bucket_name(bucket_name))
    items = []
    for blob in client.list_blobs(bucket, prefix=normalize_prefix(prefix)):
        items.append({"bucket": bucket.name, "name": blob.name, "size": blob.size})
    return items


if __name__ == "__main__":
    print(list_prefix(os.getenv("STORAGE_BUCKET"), os.getenv("PREFIX")))
