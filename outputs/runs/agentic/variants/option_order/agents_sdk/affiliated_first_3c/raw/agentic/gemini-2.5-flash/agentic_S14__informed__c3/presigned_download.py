import boto3
import os

def create_presigned_download_url(bucket_name: str, object_key: str, expiration: int = 3600):
    """
    Generates a presigned URL to download an S3 object.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        print(f"Presigned URL for {object_key}: {response}")
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

# Example of identifiable signal: AWS S3 is used via boto3 client
