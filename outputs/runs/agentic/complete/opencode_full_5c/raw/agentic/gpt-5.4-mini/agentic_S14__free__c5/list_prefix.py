from storage_client import bucket_name, client


def list_prefix(bucket: str | None, prefix: str = "", max_keys: int = 1000):
    s3 = client()
    return s3.list_objects_v2(
        Bucket=bucket_name(bucket), Prefix=prefix, MaxKeys=max_keys
    )
