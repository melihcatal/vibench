import os
import boto3
from storage_client import get_s3_client


def get_object_metadata(bucket_name, key):
    """Retrieve metadata (head) for an object in Amazon S3.

    Uses boto3 SDK and authenticates via AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.
    Returns the HEAD response dictionary.
    """
    s3_client = get_s3_client()
    return s3_client.head_object(Bucket=bucket_name, Key=key)
