import os
from storage_client import get_s3_client
from storage_models import normalize_head_params

def get_object_metadata(bucket, key):
    """Retrieves metadata/HEAD information for an object stored in Amazon S3.
    Uses boto3 S3 client from storage_client.py.
    Returns a dict with the response metadata.
    """
    params = normalize_head_params(bucket, key)
    s3 = get_s3_client()
    response = s3.head_object(**params)
    print(f'Fetched metadata for {key} in bucket {bucket}.')
    return response
