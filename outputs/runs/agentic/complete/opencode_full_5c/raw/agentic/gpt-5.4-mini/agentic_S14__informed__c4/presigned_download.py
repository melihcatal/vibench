from storage_client import client


def presigned_download(bucket: str, key: str, expires_in: int = 900) -> str:
    s3 = client()
    return s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_in
    )
