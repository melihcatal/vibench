import boto3

from storage_client import get_s3_client


def get_object_metadata(object_name):
    client = get_s3_client()
    response = client.head_object(Bucket='your-bucket-name', Key=object_name)
    return response