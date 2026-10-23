import boto3
import os

def archive_metric_snapshot(file_path, bucket_name, object_name=None):
    """
    Archives a metric snapshot to Amazon S3.

    :param file_path: Path to the file to upload
    :param bucket_name: S3 bucket to upload to
    :param object_name: S3 object name. If not specified then file_path is used
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Initialize S3 client (AWS SDK for Python - boto3)
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    # Example usage:
    # Replace 'your-metric-snapshot.json' with the actual path to your metric snapshot file
    # Replace 'your-s3-bucket-name' with your actual S3 bucket name
    
    # Create a dummy file for demonstration purposes
    dummy_file_name = "dummy_metric_snapshot.json"
    with open(dummy_file_name, "w") as f:
        f.write('''{"timestamp": "2023-10-27T10:00:00Z", "metric_data": {"cpu_usage": 0.5, "memory_usage": 0.7}}''')

    archive_metric_snapshot(dummy_file_name, "your-s3-bucket-name")
    
    # Clean up the dummy file
    os.remove(dummy_file_name)
