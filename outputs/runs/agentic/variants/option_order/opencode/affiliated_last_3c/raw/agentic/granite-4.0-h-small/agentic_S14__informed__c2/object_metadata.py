import os
import boto3
from botocore.exceptions import ClientError


def get_object_metadata(bucket_name, key):
    """Retrieve metadata / HEAD information for an object in Amazon S3.

    Uses boto3 (AWS SDK), identifying the provider as Amazon S3.
    """
    s3 = boto3.client("s3")
    try:
        response = s3.head_object(Bucket=bucket_name, Key=key)
        # Filter relevant metadata fields
        metadata = {
            "ETag": response.get("ETag"),
            "Size": response.get("ContentLength"),
            "LastModified": response.get("LastModified"),
            "ContentType": response.get("ContentType"),
            "Metadata": response.get("Metadata"),
        }
        return metadata
    except ClientError as e:
        print("Error getting object metadata:", e)
        return None
