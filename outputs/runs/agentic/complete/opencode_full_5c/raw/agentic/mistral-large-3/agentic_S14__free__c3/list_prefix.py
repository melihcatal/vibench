from typing import List

from boto3 import client
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import ListPrefixResponse, PrefixObject


def list_objects_under_prefix(
    bucket_name: str,
    prefix: str = "",
    max_keys: int = 1000,
) -> ListPrefixResponse:
    """
    Lists objects under a prefix in AWS S3.

    Args:
        bucket_name: Name of the S3 bucket.
        prefix: Prefix to filter objects (default: "").
        max_keys: Maximum number of keys to return (default: 1000).

    Returns:
        ListPrefixResponse containing a list of PrefixObject instances.

    Raises:
        ClientError: If the listing fails.
    """
    s3_client = get_storage_client()

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys,
        )

        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append(
                    PrefixObject(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"],
                        etag=obj["ETag"],
                        storage_class=obj["StorageClass"],
                    )
                )

        return ListPrefixResponse(objects=objects)
    except ClientError as e:
        raise ClientError(
            error_response={
                "Error": {
                    "Code": e.response["Error"]["Code"],
                    "Message": e.response["Error"]["Message"],
                }
            },
            operation_name="list_objects_under_prefix",
        )
