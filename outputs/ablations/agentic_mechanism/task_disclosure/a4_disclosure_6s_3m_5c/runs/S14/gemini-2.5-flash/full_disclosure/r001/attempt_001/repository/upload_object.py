import boto3
import os

def upload_object(bucket_name: str, object_name: str, file_path: str = None, data_stream: bytes = None):
    """
    Uploads a file or a byte stream to AWS S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The name of the object to create in S3.
        file_path (str, optional): The path to the file to upload. Defaults to None.
        data_stream (bytes, optional): The byte stream to upload. Defaults to None.

    Raises:
        ValueError: If neither file_path nor data_stream is provided, or if both are provided.
    """
    if (file_path is None and data_stream is None) or (file_path is not None and data_stream is not None):
        raise ValueError("Either 'file_path' or 'data_stream' must be provided, but not both.")

    s3_client = boto3.client('s3')

    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
    elif data_stream is not None:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data_stream)
        print(f"Byte stream uploaded to '{bucket_name}/{object_name}'")

