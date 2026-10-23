import os
from storage_client import get_s3_client

def get_object_metadata(bucket_name, object_key):
    """Retrieve metadata / HEAD information for an object in Amazon S3.
    Returns a dict of metadata returned by boto3's head_object.
    """
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    return response
