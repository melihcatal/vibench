from storage_client import create_aws_client
from storage_models import ObjectMetadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    client = create_aws_client("s3")
    resp = client.head_object(Bucket=bucket, Key=key)
    return {
        "content_type": resp.get("ContentType"),
        "content_length": resp["ContentLength"],
        "last_modified": resp["LastModified"].isoformat()
        if "LastModified" in resp
        else None,
        "metadata": dict(resp.get("Metadata", {})),
    }
