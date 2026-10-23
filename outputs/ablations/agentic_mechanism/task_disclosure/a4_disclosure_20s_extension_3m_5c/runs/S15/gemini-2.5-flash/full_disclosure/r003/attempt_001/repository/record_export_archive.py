import boto3
import os

def archive_document_to_s3(file_path: str, bucket_name: str, object_key: str):
    """
    Archives a document (snapshot or attachment) to AWS S3 managed object storage.

    Args:
        file_path (str): The local path to the file to be archived.
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The desired key (path) for the object in the S3 bucket.
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"File '{file_path}' successfully archived to s3://{bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error archiving file to S3: {e}")

