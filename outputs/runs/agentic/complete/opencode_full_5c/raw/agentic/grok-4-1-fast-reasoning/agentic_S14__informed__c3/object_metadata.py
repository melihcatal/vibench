from storage_client import get_s3_client, get_bucket
from storage_models import ObjectMetadata
from botocore.exceptions import ClientError


def get_object_metadata(key: str) -> ObjectMetadata:
    client = get_s3_client()
    bucket = get_bucket()
    try:
        resp = client.head_object(Bucket=bucket, Key=key)
        return ObjectMetadata(
            size=resp["ContentLength"],
            etag=resp["ETag"],
            last_modified=resp["LastModified"],
            content_type=resp.get("ContentType"),
        )
    except ClientError:
        raise ValueError(f"Metadata retrieval failed for key: {key}")
