import os
import boto3


def create_presigned_download_url(bucket: str, object_key: str, expires_in: int = 3600, region_name: str | None = None) -> str:
    session = boto3.session.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    client = session.client("s3")
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": object_key},
        ExpiresIn=expires_in,
    )


def main() -> None:
    bucket = os.environ["S3_BUCKET"]
    object_key = os.environ["S3_OBJECT_KEY"]
    expires_in = int(os.getenv("S3_PRESIGN_EXPIRES_IN", "3600"))
    print(create_presigned_download_url(bucket, object_key, expires_in))


if __name__ == "__main__":
    main()
