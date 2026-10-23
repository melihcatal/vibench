from storage_client import build_metadata_response, get_s3_client


def object_metadata(bucket: str, key: str):
    client = get_s3_client()
    head = client.head_object(Bucket=bucket, Key=key)
    return build_metadata_response(bucket, key, head)
