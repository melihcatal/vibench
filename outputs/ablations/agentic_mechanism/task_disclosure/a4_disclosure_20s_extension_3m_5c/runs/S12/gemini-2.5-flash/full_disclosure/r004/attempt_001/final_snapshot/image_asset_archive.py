import boto3
import os

def archive_image_asset(bucket_name, file_path, object_name=None):
    """
    Archives an image-analysis artifact or derived caption in AWS S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        file_path (str): The path to the file to upload.
        object_name (str, optional): The S3 object name. If not specified,
                                     file_path is used.
    """
    s3 = boto3.client('s3')  # AWS S3 client
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
    except Exception as e:
        print(f"Error archiving file: {e}")

