import boto3
import os

def create_presigned_download_url(bucket_name: str, object_name: str, expiration_seconds: int = 3600):
    """
    Generates a presigned URL for downloading an S3 object.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name,'Key': object_name},
            ExpiresIn=expiration_seconds
        )
        print(f"Presigned URL for {bucket_name}/{object_name}: {response}")
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

