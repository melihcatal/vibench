import os
import boto3

def archive_image_assets(
    file_path: str,
    bucket_name: str,
    object_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    region_name: str = 'us-east-1'
):
    """
    Archives image-analysis artifacts and derived captions in AWS S3.

    Args:
        file_path (str): The path to the file to upload.
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The desired object name in the S3 bucket.
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        region_name (str): The AWS region name (default: 'us-east-1').
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
    except Exception as e:
        print(f"Error archiving file to S3: {e}")

