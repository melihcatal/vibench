import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import get_s3_client
from storage_models import ObjectMetadata


def get_object_metadata(
    bucket_name: str, object_name: str
) -> Optional[ObjectMetadata]:
    """
    Retrieves metadata for an object in an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The name of the object in the bucket.
    :return: An ObjectMetadata object, or None if the object does not exist.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
        metadata = ObjectMetadata(
            object_key=object_name,
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength"),
            last_modified=response.get("LastModified"),
            etag=response.get("ETag", "").strip('"'),
            custom_metadata=response.get("Metadata", {}),
        )
        return metadata
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Object '{object_name}' not found in bucket '{bucket_name}'.")
        else:
            print(f"An error occurred: {e}")
        return None
