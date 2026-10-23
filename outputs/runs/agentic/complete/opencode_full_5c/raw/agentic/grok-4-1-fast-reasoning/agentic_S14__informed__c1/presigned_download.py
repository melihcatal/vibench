from storage_client import s3_config
import boto3


def create_presigned_download_url(bucket: str, key: str, expiration: int = 3600) -> str:
    client = boto3.client("s3", **s3_config)
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration,
    )
    return url
