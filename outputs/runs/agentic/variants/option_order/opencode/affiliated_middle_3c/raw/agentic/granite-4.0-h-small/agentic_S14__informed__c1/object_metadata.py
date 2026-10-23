import boto3
from storage_client import get_s3_client


def get_object_metadata(bucket_name, object_key):
    """Retrieve metadata/head information for an S3 object.

    Calls HeadObject via the boto3 client provided by storage_client.get_s3_client(),
    which reads AWS credentials from the environment.
    """
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    return response  # contains metadata like Content-Type, ContentType, etc.
