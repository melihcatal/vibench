from storage_client import get_s3_client, get_bucket


def create_presigned_url(key: str, expiration_seconds: int = 3600) -> str:
    client = get_s3_client()
    bucket = get_bucket()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration_seconds,
    )
