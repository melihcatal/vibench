import os
from datetime import timedelta

from google.cloud import storage


def create_presigned_download_url(bucket_name: str, object_name: str, expires_in_seconds: int = 3600) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    return blob.generate_signed_url(expiration=timedelta(seconds=expires_in_seconds), method="GET", version="v4")


def main() -> None:
    bucket_name = os.environ["GCS_BUCKET_NAME"]
    object_name = os.environ["GCS_OBJECT_NAME"]
    expires_in_seconds = int(os.getenv("PRESIGNED_URL_EXPIRES_IN_SECONDS", "3600"))
    print(create_presigned_download_url(bucket_name, object_name, expires_in_seconds))


if __name__ == "__main__":
    main()
