import os
from datetime import timedelta

from google.cloud import storage


def create_presigned_download_url(bucket_name: str, blob_name: str, expiration_seconds: int = 3600) -> str:
    client = storage.Client()
    blob = client.bucket(bucket_name).blob(blob_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=expiration_seconds),
        method="GET",
    )


def main() -> None:
    bucket_name = os.environ["GCS_BUCKET_NAME"]
    blob_name = os.environ["GCS_OBJECT_NAME"]
    expiration_seconds = int(os.getenv("SIGNED_URL_EXPIRATION_SECONDS", "3600"))
    print(create_presigned_download_url(bucket_name, blob_name, expiration_seconds))


if __name__ == "__main__":
    main()
