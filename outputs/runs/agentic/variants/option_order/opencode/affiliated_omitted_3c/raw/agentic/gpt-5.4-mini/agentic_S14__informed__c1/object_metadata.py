from storage_client import get_s3_client, resolve_bucket


def object_metadata(bucket, key):
    client = get_s3_client()
    return client.head_object(Bucket=resolve_bucket(bucket), Key=key)
