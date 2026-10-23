import os
import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

def archive_metrics_snapshot(
    bucket_name: str, 
    metric_data: dict, 
    region_name: str = "us-east-1"
) -> str:
    """
    Archives exported metric snapshots in Amazon S3.

    Args:
        bucket_name: The name of the S3 bucket.
        metric_data: The metric data to be archived (as a dictionary).
        region_name: The AWS region of the bucket.

    Returns:
        The S3 object key for the archived file.
    """
    s3_client = boto3.client(
        "s3",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    object_key = f"metrics-snapshot-{timestamp}.json"
    
    try:
        # Convert dict to JSON string for upload
        json_data = json.dumps(metric_data, indent=2)
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_data,
            ContentType="application/json"
        )
        return object_key
    except ClientError as e:
        # Handle potential errors, e.g., bucket not found, permissions
        raise RuntimeError(f"Failed to upload to S3: {e}") from e
    except TypeError as e:
        raise TypeError(f"Failed to serialize metric_data to JSON: {e}") from e
