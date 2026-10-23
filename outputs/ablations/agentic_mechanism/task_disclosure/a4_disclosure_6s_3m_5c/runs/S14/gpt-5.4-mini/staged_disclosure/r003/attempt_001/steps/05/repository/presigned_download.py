import os
from datetime import timedelta

import boto3


def create_presigned_download_url(bucket_name: str, object_key: str, expires_in_seconds: int = 3600) -> str:
    s3_client = boto3.client("s3")
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expires_in_seconds,
    )


if __name__ == "__main__":
    bucket = os.environ["AWS_S3_BUCKET"]
    key = os.environ["AWS_S3_KEY"]
    ttl = int(os.environ.get("AWS_S3_URL_TTL_SECONDS", str(int(timedelta(hours=1).total_seconds()))))
    print(create_presigned_download_url(bucket, key, ttl))
