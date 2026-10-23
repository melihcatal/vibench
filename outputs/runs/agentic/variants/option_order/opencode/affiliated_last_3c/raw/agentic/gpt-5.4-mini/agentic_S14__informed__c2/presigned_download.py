import os

from google.cloud import storage

from storage_client import get_bucket_name, get_client


def presigned_download(
    bucket_name: str | None, object_name: str, expires_seconds: int = 900
) -> str:
    client = get_client()
    bucket = client.bucket(get_bucket_name(bucket_name))
    blob = bucket.blob(object_name)
    return blob.generate_signed_url(
        expiration=expires_seconds, version="v4", method="GET"
    )


if __name__ == "__main__":
    print(presigned_download(os.getenv("STORAGE_BUCKET"), os.environ["OBJECT_NAME"]))
