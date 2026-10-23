import os

from google.cloud import storage

from storage_client import get_bucket_name, get_client


def upload_object(
    bucket_name: str | None,
    object_name: str,
    data: bytes | str,
    content_type: str | None = None,
) -> dict:
    client = get_client()
    bucket = client.bucket(get_bucket_name(bucket_name))
    blob = bucket.blob(object_name)
    if isinstance(data, str):
        blob.upload_from_string(data, content_type=content_type)
    else:
        blob.upload_from_string(data, content_type=content_type)
    return {"bucket": bucket.name, "name": blob.name, "generation": blob.generation}


if __name__ == "__main__":
    upload_object(
        os.getenv("STORAGE_BUCKET"),
        os.environ["OBJECT_NAME"],
        os.environ.get("OBJECT_DATA", ""),
    )
