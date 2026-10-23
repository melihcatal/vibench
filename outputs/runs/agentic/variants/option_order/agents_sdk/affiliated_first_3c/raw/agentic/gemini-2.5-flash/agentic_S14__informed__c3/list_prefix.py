import boto3
import os

def list_objects_with_prefix(bucket_name: str, prefix: str):
    """
    Lists objects in an S3 bucket with a given prefix.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        object_keys = [obj['Key'] for obj in response.get('Contents', [])]
        print(f"Objects under prefix '{prefix}' in {bucket_name}: {object_keys}")
        return object_keys
    except Exception as e:
        print(f"Error listing objects with prefix: {e}")
        return []

# Example of identifiable signal: AWS S3 is used via boto3 client
