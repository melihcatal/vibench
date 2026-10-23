import os
from storage_client import create_aws_s3_client
from storage_models import S3HeadObjectResult

def object_metadata(bucket_name, object_key):
    """Read metadata/head information for an object stored in S3.

    Returns S3HeadObjectResult containing metadata fields such as ContentType, Size, LastModified.
    """
    client = create_aws_s3_client()
    response = client.head_object(Bucket=bucket_name, Key=object_key)
    # Filter out only the useful metadata fields
    metadata = {
        'ContentType': response.get('ContentType'),
        'ContentLength': response.get('ContentLength'),
        'LastModified': response.get('LastModified'),
        'ETag': response.get('ETag'),
    }
    return S3HeadObjectResult(bucket=bucket_name, key=object_key, metadata=metadata)
