import boto3
import os

def archive_metric_snapshot(file_path: str, bucket_name: str, object_name: str = None, region_name: str = 'us-east-1'):
    """
    Archives an exported metric snapshot to AWS S3.

    :param file_path: Path to the file to upload.
    :param bucket_name: S3 bucket name to upload to.
    :param object_name: S3 object name. If not specified, file_path is used.
    :param region_name: AWS region where the S3 bucket is located.
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client('s3', region_name=region_name)
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == '__main__':
    # Example usage (replace with actual file path, bucket name, and region)
    # archive_metric_snapshot('path/to/your/metric_snapshot.json', 'your-s3-bucket-name', region_name='your-aws-region')
    pass
