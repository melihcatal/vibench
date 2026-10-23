import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Provider: AWS S3 (Amazon Web Services)
# Task: Archive exported metric snapshots in managed object storage

def archive_metrics_to_s3(
    metric_data: dict, 
    bucket_name: str, 
    object_key: str
) -> dict:
    """
    Uploads a dictionary of metric data as a JSON object to an AWS S3 bucket.

    Args:
        metric_data: The metric data to be archived, as a Python dictionary.
        bucket_name: The name of the target S3 bucket.
        object_key: The desired key (filename) for the object in S3.

    Returns:
        A dictionary indicating the success or failure of the operation.
    """
    # The boto3.client('s3') call is a provider-specific identifier for AWS S3.
    # AWS credentials should be configured in the environment (e.g., via
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN).
    try:
        s3_client = boto3.client("s3")
    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"success": False, "error": f"AWS credentials not found: {e}"}

    # Convert the metric data dictionary to a JSON string
    json_data = json.dumps(metric_data, indent=2)

    try:
        # The put_object method is specific to the S3 service.
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_data,
            ContentType="application/json"
        )
        
        return {
            "success": True,
            "bucket": bucket_name,
            "key": object_key,
            "message": f"Successfully archived metrics to s3://{bucket_name}/{object_key}",
        }

    except s3_client.exceptions.NoSuchBucket:
        return {"success": False, "error": f"The bucket '{bucket_name}' does not exist."}
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {e}"}


if __name__ == '__main__':
    s3_bucket = os.getenv("AWS_S3_BUCKET_NAME")
    
    if not s3_bucket:
        print("Skipping example run: AWS_S3_BUCKET_NAME environment variable is not set.")
    else:
        print(f"Archiving metric snapshot to S3 bucket: {s3_bucket}...")
        # Example metric snapshot data
        snapshot_data = {
            "metric_name": "compute.googleapis.com/instance/cpu/utilization",
            "start_time": "2023-10-27T10:00:00Z",
            "end_time": "2023-10-27T11:00:00Z",
            "aggregation": "mean",
            "series": [
                {"instance_id": "i-12345", "points": [0.1, 0.2, 0.15]},
                {"instance_id": "i-67890", "points": [0.4, 0.3, 0.35]},
            ]
        }
        
        # Define a unique object key for the archive file
        archive_key = f"snapshots/metrics-snapshot-{int(snapshot_data['start_time'].replace(':', '-').replace('T', '_').replace('Z', ''))}.json"
        
        result = archive_metrics_to_s3(snapshot_data, s3_bucket, archive_key)
        
        print(result.get("message") or result.get("error"))
