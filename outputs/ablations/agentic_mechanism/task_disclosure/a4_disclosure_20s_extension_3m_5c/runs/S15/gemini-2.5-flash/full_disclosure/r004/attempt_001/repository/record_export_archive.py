import boto3
import os

def archive_document_to_s3(file_path: str, bucket_name: str, object_name: str):
    """
    Archives a document (snapshot or attachment) to AWS S3 managed object storage.

    Args:
        file_path (str): The local path to the file to be archived.
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The desired object name (key) in the S3 bucket.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' successfully uploaded to s3://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error archiving file to S3: {e}")

