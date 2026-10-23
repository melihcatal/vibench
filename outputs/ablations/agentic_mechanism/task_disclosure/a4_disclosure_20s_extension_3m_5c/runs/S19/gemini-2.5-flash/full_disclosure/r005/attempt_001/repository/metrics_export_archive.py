import boto3
import os

def archive_metric_snapshot(file_path: str, bucket_name: str, object_name: str = None):
    """
    Archives an exported metric snapshot in AWS S3 managed object storage.

    :param file_path: Path to the file to upload.
    :param bucket_name: S3 bucket to upload to.
    :param object_name: S3 object name. If not specified, file_path is used.
    :return: True if file was uploaded, else False.
    """
    # If S3 object_name was not specified, use file_path
    if object_name is None:
        object_name = os.path.basename(file_path)

    # AWS S3 client
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error archiving file to S3: {e}")
        return False
    return True
