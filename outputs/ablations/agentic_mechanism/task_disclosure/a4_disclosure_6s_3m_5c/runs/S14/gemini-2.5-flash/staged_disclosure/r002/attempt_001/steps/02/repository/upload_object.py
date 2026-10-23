import boto3
import os

def upload_object(bucket_name, object_name, file_path=None, data_stream=None):
    """
    Uploads a file or byte stream to an S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name (key).
    :param file_path: Path to the file to upload.
    :param data_stream: Byte stream to upload.
    """
    s3_client = boto3.client('s3')

    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
    elif data_stream:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data_stream)
        print(f"Byte stream uploaded to '{bucket_name}/{object_name}'")
    else:
        raise ValueError("Either 'file_path' or 'data_stream' must be provided.")

