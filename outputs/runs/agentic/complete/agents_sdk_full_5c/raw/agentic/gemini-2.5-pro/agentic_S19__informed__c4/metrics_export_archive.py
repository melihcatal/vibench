import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from datetime import datetime

def archive_metrics_to_s3(
    bucket_name: str,
    metric_data: dict,
    snapshot_name: str,
) -> bool:
    """
    Archives a snapshot of metric data to Amazon S3.

    Args:
        bucket_name: The name of the S3 bucket.
        metric_data: A dictionary containing the metric data to archive.
        snapshot_name: A descriptive name for the snapshot.

    Returns:
        True if the upload was successful, False otherwise.
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: AWS credentials not found. {e}")
        return False
        
    timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    object_key = f"metrics-archive/{snapshot_name}/{timestamp}.json"
    
    # Convert the metric data dictionary to a JSON string
    json_data = json.dumps(metric_data, indent=2)
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_data,
            ContentType='application/json'
        )
        print(f"Successfully archived '{object_key}' to S3 bucket '{bucket_name}'.")
        return True
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        print(f"Failed to upload to S3. Error Code: {error_code}, Message: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == '__main__':
    s3_bucket = os.getenv("AWS_S3_BUCKET_NAME")
    if not s3_bucket:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable is not set.")

    # Example metric snapshot data
    cpu_usage_snapshot = {
        "metric_name": "compute.googleapis.com/instance/cpu/usage_time",
        "time_range": "2023-10-27T10:00:00Z to 2023-10-27T11:00:00Z",
        "instance_id": "i-12345abcdef",
        "aggregated_value": 0.85,
        "unit": "percentage"
    }

    archive_metrics_to_s3(
        bucket_name=s3_bucket,
        metric_data=cpu_usage_snapshot,
        snapshot_name="prod-db-cpu-incident-24"
    )
