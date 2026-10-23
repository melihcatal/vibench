import boto3
import os

def archive_document_to_s3(file_path: str, bucket_name: str, object_name: str):
    """
    Archives a document snapshot or attachment to Amazon S3.

    Args:
        file_path (str): The local path to the file to upload.
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The desired object name (key) in the S3 bucket.
    """
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' successfully uploaded to s3://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error archiving file to S3: {e}")

