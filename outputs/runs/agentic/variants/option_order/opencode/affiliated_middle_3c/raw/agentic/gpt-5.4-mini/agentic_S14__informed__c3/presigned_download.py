import boto3

from storage_client import resolve_bucket


def create_presigned_download_url(bucket: str, key: str, expires_in: int = 3600):
    client = boto3.client("s3")
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": resolve_bucket(bucket), "Key": key},
        ExpiresIn=expires_in,
    )
