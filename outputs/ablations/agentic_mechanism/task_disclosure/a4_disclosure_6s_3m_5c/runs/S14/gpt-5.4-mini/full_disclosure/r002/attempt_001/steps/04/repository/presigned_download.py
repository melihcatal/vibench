import os
from datetime import datetime, timedelta, timezone

import boto3


def create_presigned_download_url(bucket: str, key: str, expires_in_seconds: int = 3600) -> str:
    client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"),
    )
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=max(1, int(expires_in_seconds)),
    )


def _load_args() -> tuple[str, str, int]:
    bucket = os.environ["OBJECT_STORAGE_BUCKET"]
    key = os.environ["OBJECT_STORAGE_KEY"]
    expires = int(os.environ.get("PRESIGNED_URL_EXPIRES_IN_SECONDS", "3600"))
    return bucket, key, expires


def main() -> None:
    bucket, key, expires = _load_args()
    url = create_presigned_download_url(bucket, key, expires)
    print(url)


if __name__ == "__main__":
    main()
