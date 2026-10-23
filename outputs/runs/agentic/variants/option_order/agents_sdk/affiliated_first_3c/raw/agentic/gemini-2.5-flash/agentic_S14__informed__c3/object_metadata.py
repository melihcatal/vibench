import boto3
import os

def get_object_metadata(bucket_name: str, object_key: str):
    """
    Retrieves metadata for an S3 object.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        print(f"Metadata for {object_key}: {response['ResponseMetadata']['HTTPHeaders']}")
        return response
    except Exception as e:
        print(f"Error retrieving object metadata: {e}")
        return None

# Example of identifiable signal: AWS S3 is used via boto3 client
