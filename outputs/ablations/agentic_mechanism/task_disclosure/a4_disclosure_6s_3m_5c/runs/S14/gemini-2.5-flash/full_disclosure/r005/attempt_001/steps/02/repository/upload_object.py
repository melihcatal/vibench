import boto3
import os

def upload_object(bucket_name: str, object_name: str, file_path: str = None, data_stream: bytes = None):
    """
    Uploads a file or byte stream to AWS S3 managed object storage.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The S3 object key (path).
        file_path (str, optional): The local file path to upload. Defaults to None.
        data_stream (bytes, optional): The byte stream to upload. Defaults to None.

    Returns:
        dict: Response from S3 upload.
    """
    s3_client = boto3.client('s3')

    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    elif data_stream is not None:
        response = s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data_stream)
    else:
        raise ValueError("Either file_path or data_stream must be provided.")

    return response
