from storage_client import load_storage_config, s3_client


def presigned_download(bucket: str, key: str, expires_in: int = 900):
    config = load_storage_config(bucket)
    client = s3_client()
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": config.bucket, "Key": key},
        ExpiresIn=expires_in,
    )
