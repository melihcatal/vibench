import boto3

from storage_client import resolve_bucket


def list_objects_with_prefix(bucket: str, prefix: str = ""):
    client = boto3.client("s3")
    response = client.list_objects_v2(Bucket=resolve_bucket(bucket), Prefix=prefix)
    return [item["Key"] for item in response.get("Contents", [])]
