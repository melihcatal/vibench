import boto3

from storage_client import get_s3_client


def get_object_metadata(object_name):
    client = get_s3_client()
    try:
        response = client.head_object(Bucket='your-bucket-name', Key=object_name)
    except client.exceptions.ClientError as e:
        raise e
    return response