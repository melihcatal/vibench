import boto3
import os
import json
from datetime import datetime

def archive_metric_snapshot(snapshot_data: dict, bucket_name: str, object_key_prefix: str = "metric_snapshots/"):
    """
    Archives exported metric snapshots in AWS S3 managed object storage.

    Args:
        snapshot_data (dict): The metric snapshot data to be archived.
        bucket_name (str): The name of the S3 bucket to store the snapshots.
        object_key_prefix (str): The prefix for the S3 object key.
    """
    s3_client = boto3.client("s3")

    # Generate a unique object key using a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    object_key = f"{object_key_prefix}metric_snapshot_{timestamp}.json"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json.dumps(snapshot_data),
            ContentType="application/json"
        )
        print(f"Metric snapshot successfully archived to s3://{bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error archiving metric snapshot to S3: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set your AWS credentials as environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # or configure them using ~/.aws/credentials
    
    # Replace with your S3 bucket name
    S3_BUCKET_NAME = os.environ.get("S3_METRIC_ARCHIVE_BUCKET", "your-metric-archive-bucket-name")

    example_snapshot = {
        "metric_name": "cpu_utilization",
        "timestamp": "2026-09-20T10:00:00Z",
        "value": 0.45,
        "dimensions": {
            "instance_id": "i-1234567890abcdef0",
            "region": "us-east-1"
        }
    }

    archive_metric_snapshot(example_snapshot, S3_BUCKET_NAME)
