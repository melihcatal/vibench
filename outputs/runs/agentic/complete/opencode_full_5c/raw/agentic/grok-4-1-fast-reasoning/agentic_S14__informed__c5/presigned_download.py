from storage_client import get_s3_client


def presigned_download(
    bucket_name: str, object_name: str, expiration: int = 3600
) -> str:
    client = get_s3_client()
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expiration,
    )
    return url
