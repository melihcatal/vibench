from storage_client import get_bucket_name, get_s3_client


def object_metadata(key: str) -> dict:
    return get_s3_client().head_object(Bucket=get_bucket_name(), Key=key)
