import os
from datetime import timedelta

import boto3


def create_presigned_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    client = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=int(timedelta(seconds=expires_in).total_seconds()),
    )


def main() -> None:
    bucket = os.environ["S3_BUCKET"]
    key = os.environ["S3_KEY"]
    expires_in = int(os.getenv("PRESIGNED_URL_EXPIRES_IN", "3600"))
    print(create_presigned_download_url(bucket, key, expires_in))


if __name__ == "__main__":
    main()
