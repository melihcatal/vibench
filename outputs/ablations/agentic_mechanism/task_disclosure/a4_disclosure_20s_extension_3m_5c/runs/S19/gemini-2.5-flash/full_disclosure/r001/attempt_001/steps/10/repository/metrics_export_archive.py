import boto3
import os

def archive_metric_snapshot(file_path: str, bucket_name: str, object_name: str = None):
    """
    Archives a metric snapshot file to AWS S3 managed object storage.

    Args:
        file_path (str): The path to the file to upload.
        bucket_name (str): The name of the S3 bucket to upload to.
        object_name (str, optional): The S3 object name. If not specified,
                                     file_path is used.
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client('s3')
    s3_client.upload_file(file_path, bucket_name, object_name)
    print(f"File {file_path} uploaded to s3://{bucket_name}/{object_name}")

# Example of how AWS S3 is identifiable in code:
# - import boto3
# - boto3.client('s3')
