import boto3
import os

def list_objects_with_prefix(bucket_name: str, prefix: str):
    """
    Lists objects in an S3 bucket under a given prefix.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        object_keys = []
        if 'Contents' in response:
            for obj in response['Contents']:
                object_keys.append(obj['Key'])
        print(f"Objects under prefix '{prefix}' in bucket '{bucket_name}': {object_keys}")
        return object_keys
    except Exception as e:
        print(f"Error listing objects with prefix: {e}")
        return []

