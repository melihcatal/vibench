import os

import boto3


def create_presigned_download_url(bucket_name: str, object_key: str, *, expires_in: int = 3600, region_name: str | None = None) -> str:
    s3 = boto3.client("s3", region_name=region_name)
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expires_in,
    )


def main() -> None:
    bucket_name = os.environ["S3_BUCKET_NAME"]
    object_key = os.environ["S3_OBJECT_KEY"]
    expires_in = int(os.environ.get("S3_PRESIGNED_EXPIRES_IN", "3600"))
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    print(create_presigned_download_url(bucket_name, object_key, expires_in=expires_in, region_name=region_name))


if __name__ == "__main__":
    main()
