import boto3
from botocore.exceptions import NoCredentialsError

def upload_object(file_path: str = None, bucket_name: str = None, object_key: str = None, data_stream: bytes = None):
    """
    Uploads a file or a byte stream to AWS S3.

    Args:
        file_path (str): The path to the file to upload.
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The S3 object key (path) in the bucket.
        data_stream (bytes): A byte stream to upload.
    """
    if not bucket_name or not object_key:
        raise ValueError("bucket_name and object_key are required.")

    if file_path is None and data_stream is None:
        raise ValueError("Either file_path or data_stream must be provided.")
    if file_path is not None and data_stream is not None:
        raise ValueError("Only one of file_path or data_stream should be provided.")

    s3 = boto3.client('s3')

    try:
        if file_path:
            s3.upload_file(file_path, bucket_name, object_key)
            return f"File '{file_path}' uploaded to s3://{bucket_name}/{object_key}"
        elif data_stream:
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=data_stream)
            return f"Byte stream uploaded to s3://{bucket_name}/{object_key}"
    except NoCredentialsError:
        raise Exception("AWS credentials not found. Please configure your AWS credentials.")
    except Exception as e:
        raise Exception(f"Error uploading object to S3: {e}")
