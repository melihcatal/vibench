import os
import boto3
from botocore.exceptions import NoCredentialsError

def archive_metric_snapshot(file_path: str, bucket_name: str, object_name: str = None):
    """
    Archives a metric snapshot file to AWS S3.

    :param file_path: Path to the file to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name. If not specified, file_path is used.
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3 = boto3.client('s3')

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_path} was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set your AWS credentials as environment variables or configure them
    # via the AWS CLI.
    # AWS_ACCESS_KEY_ID
    # AWS_SECRET_ACCESS_KEY
    # AWS_REGION

    # Create a dummy file for demonstration
    dummy_file_name = "metric_snapshot_2026-09-20.json"
    with open(dummy_file_name, "w") as f:
        f.write('''{
    "timestamp": "2026-09-20T10:00:00Z",
    "metrics": {
        "cpu_usage": "50%",
        "memory_free": "2GB"
    }
}''')

    # Replace with your S3 bucket name
    s3_bucket_name = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name")

    archive_metric_snapshot(dummy_file_name, s3_bucket_name)

    # Clean up dummy file
    os.remove(dummy_file_name)
