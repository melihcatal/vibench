from storage_client import bucket_name, client


def presigned_download(bucket: str | None, key: str, expires_in: int = 900):
    s3 = client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name(bucket), "Key": key},
        ExpiresIn=expires_in,
    )
