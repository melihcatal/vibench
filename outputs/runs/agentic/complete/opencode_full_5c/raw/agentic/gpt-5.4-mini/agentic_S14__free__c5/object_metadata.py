from storage_client import bucket_name, client


def object_metadata(bucket: str | None, key: str):
    s3 = client()
    return s3.head_object(Bucket=bucket_name(bucket), Key=key)
