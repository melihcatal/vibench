import boto3
from storage_client import get_s3_client


def upload_object(bucket_name, object_key, data, **kwargs):
    """Upload a file or byte stream to S3 object storage.

    Uses boto3 client obtained from storage_client.get_s3_client(), which
    reads AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    s3 = get_s3_client()
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=data, **kwargs)
