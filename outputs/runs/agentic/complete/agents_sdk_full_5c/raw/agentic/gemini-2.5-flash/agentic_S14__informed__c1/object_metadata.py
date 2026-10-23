import boto3
import os

def get_object_metadata(bucket_name: str, object_name: str):
    """
    Retrieves metadata for an S3 object.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
        print(f"Metadata for {bucket_name}/{object_name}: {response['ResponseMetadata']['HTTPHeaders']}")
        return response
    except Exception as e:
        print(f"Error retrieving object metadata: {e}")
        return None

