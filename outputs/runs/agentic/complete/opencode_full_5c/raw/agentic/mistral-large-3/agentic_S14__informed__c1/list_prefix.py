import boto3
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import ListPrefixResponse, ListedObject


def list_objects_with_prefix(
    bucket_name: str,
    prefix: str = "",
    max_keys: int = 1000,
) -> ListPrefixResponse:
    """
    Lists objects in an Amazon S3 bucket under a given prefix.

    Args:
        bucket_name: Name of the S3 bucket.
        prefix: Prefix to filter objects.
        max_keys: Maximum number of keys to return.

    Returns:
        ListPrefixResponse containing a list of objects under the prefix.
    """
    s3_client = get_storage_client()

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=bucket_name,
            Prefix=prefix,
            PaginationConfig={"MaxItems": max_keys},
        )

        objects = []
        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    objects.append(
                        ListedObject(
                            object_id=obj["Key"],
                            size=obj["Size"],
                            last_modified=obj["LastModified"],
                            etag=obj["ETag"].strip('"'),
                        )
                    )

        return ListPrefixResponse(
            bucket_name=bucket_name, prefix=prefix, objects=objects, provider="aws_s3"
        )
    except ClientError as e:
        raise Exception(f"Failed to list objects: {e}")
