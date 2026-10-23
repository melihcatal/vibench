from storage_client import get_storage_client


def presigned_download(bucket_name, object_name, expiration=3600):
    client = get_storage_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expiration,
    )
