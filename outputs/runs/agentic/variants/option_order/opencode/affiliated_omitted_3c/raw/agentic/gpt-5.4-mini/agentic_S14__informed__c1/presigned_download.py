from storage_client import get_s3_client, resolve_bucket


def presigned_download(bucket, key, expires_in_seconds=3600):
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": resolve_bucket(bucket), "Key": key},
        ExpiresIn=expires_in_seconds,
    )
