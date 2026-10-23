from storage_client import get_s3_client


def presigned_download(bucket: str, key: str, expiration: int = 3600) -> str:
    client = get_s3_client()
    url = client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expiration
    )
    return url
