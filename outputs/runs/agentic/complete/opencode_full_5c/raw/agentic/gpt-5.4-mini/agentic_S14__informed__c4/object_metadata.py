from storage_client import client


def object_metadata(bucket: str, key: str) -> dict:
    s3 = client()
    return s3.head_object(Bucket=bucket, Key=key)
