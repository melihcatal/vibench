from storage_client import get_bucket_name, get_s3_client


def list_prefix(prefix: str = "", max_items: int = 1000) -> list[dict]:
    response = get_s3_client().list_objects_v2(
        Bucket=get_bucket_name(), Prefix=prefix, MaxKeys=max_items
    )
    return response.get("Contents", [])
