from storage_client import get_s3_client, get_bucket_name

def create_presigned_download_url(
    bucket_name: str | None = None,
    key: str,
    expiration: int = 3600
) -> str:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    client = get_s3_client()
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=expiration
    )
    return url
