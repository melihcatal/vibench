from storage_client import build_presigned_download_response, get_s3_client


def presigned_download(bucket: str, key: str, expires_in: int = 900):
    client = get_s3_client()
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    return build_presigned_download_response(bucket, key, url, expires_in)
