import boto3
import os

def archive_metric_snapshot(file_path: str, bucket_name: str, object_name: str = None):
    """
    Archives a metric snapshot file to an Amazon S3 bucket.

    :param file_path: Path to the file to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name. If not specified, file_path is used.
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
    except Exception as e:
        print(f"Error archiving file: {e}")

if __name__ == "__main__":
    # Example usage (replace with your actual file path and bucket name)
    # create a dummy file for demonstration
    dummy_file_path = "metric_snapshot_20260920.csv"
    with open(dummy_file_path, "w") as f:
        f.write("timestamp,metric_name,value\n")
        f.write("2026-09-20T10:00:00Z,cpu_usage,50.5\n")
        f.write("2026-09-20T10:01:00Z,memory_usage,70.2\n")

    # Before running, ensure you have AWS credentials configured (e.g., via environment variables or ~/.aws/credentials)
    # and replace 'your-s3-bucket-name' with your actual bucket name.
    # archive_metric_snapshot(dummy_file_path, "your-s3-bucket-name")
    
    # Clean up dummy file
    os.remove(dummy_file_path)
