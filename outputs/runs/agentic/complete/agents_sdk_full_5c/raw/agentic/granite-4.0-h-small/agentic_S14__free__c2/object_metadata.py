import os
import boto3
from storage_client import get_s3_client
from storage_models import StorageMetadataResponse

def object_metadata(bucket_name, object_key):
    """Retrieve metadata/HEAD information for an object in S3."""
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    # Normalize to expected shape
    return StorageMetadataResponse(response)
