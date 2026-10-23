import os

from storage_client import get_bucket_name, get_client


def object_metadata(bucket_name: str | None, object_name: str) -> dict:
    client = get_client()
    blob = client.bucket(get_bucket_name(bucket_name)).get_blob(object_name)
    if blob is None:
        raise FileNotFoundError(object_name)
    blob.reload()
    return {
        "bucket": blob.bucket.name,
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "metadata": blob.metadata or {},
    }


if __name__ == "__main__":
    print(object_metadata(os.getenv("STORAGE_BUCKET"), os.environ["OBJECT_NAME"]))
