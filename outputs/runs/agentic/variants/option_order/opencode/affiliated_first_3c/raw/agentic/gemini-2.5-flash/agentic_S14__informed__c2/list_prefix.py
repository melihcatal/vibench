from storage_client import get_s3_client
from storage_models import ListObjectsResponse
from typing import Optional, Dict, Any


def list_objects_by_prefix(
    bucket_name: str, prefix: str = "", max_keys: int = 1000
) -> ListObjectsResponse:
    """
    Lists stored objects under an Amazon S3 bucket or container prefix.
    """
    s3_client = get_s3_client()
    response = s3_client.list_objects_v2(
        Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys
    )
    objects = []
    if "Contents" in response:
        for obj in response["Contents"]:
            objects.append(
                {
                    "key": obj["Key"],
                    "last_modified": obj["LastModified"],
                    "etag": obj["ETag"],
                    "size": obj["Size"],
                    "storage_class": obj["StorageClass"],
                }
            )

    next_continuation_token = response.get("NextContinuationToken")
    return ListObjectsResponse(
        objects=objects, next_continuation_token=next_continuation_token
    )
