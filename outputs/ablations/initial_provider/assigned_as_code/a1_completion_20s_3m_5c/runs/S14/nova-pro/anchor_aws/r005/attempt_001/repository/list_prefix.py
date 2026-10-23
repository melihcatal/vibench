import boto3

from storage_client import get_s3_client


def list_objects(prefix):
    s3_client = get_s3_client()
    response = s3_client.list_objects_v2(Bucket='your-bucket-name', Prefix=prefix)
    return response['Contents']