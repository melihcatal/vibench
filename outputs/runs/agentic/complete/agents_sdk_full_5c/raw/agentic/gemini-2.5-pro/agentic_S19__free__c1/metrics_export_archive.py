
import os
import json
import datetime
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def archive_metrics_to_s3(bucket_name: str, metric_data: dict, region: str = "us-east-1") -> bool:
    """
    Archives a dictionary of metric data to an AWS S3 bucket.

    The metric data is serialized to JSON and stored in a file named with
    a timestamp.

    Args:
        bucket_name: The name of the S3 bucket.
        metric_data: A dictionary containing the metric data to archive.
        region: The AWS region of the S3 bucket.

    Returns:
        True if the upload was successful, False otherwise.
    """
    # AWS credentials should be configured in the environment (e.g., via
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN).
    s3_client = boto3.client("s3", region_name=region)

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    file_name = f"metric-snapshot-{timestamp}.json"
    
    try:
        # Serialize the dictionary to a JSON string
        json_content = json.dumps(metric_data, indent=2)

        # Upload the JSON string as a file to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json_content,
            ContentType="application/json"
        )
        print(f"Successfully uploaded '{file_name}' to bucket '{bucket_name}'.")
        return True
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found. Please configure your environment.")
        return False
    except ClientError as e:
        # Handles errors like 'NoSuchBucket'
        print(f"An S3 client error occurred: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


if __name__ == "__main__":
    # Ensure the AWS S3 bucket name is set
    aws_bucket_name = os.environ.get("AWS_S3_ARCHIVE_BUCKET")
    if not aws_bucket_name:
        raise ValueError("AWS_S3_ARCHIVE_BUCKET environment variable is not set.")

    # Example metric data to be archived
    sample_metrics = {
        "timestamp_utc": datetime.datetime.utcnow().isoformat(),
        "region": "us-west-2",
        "metrics": [
            {
                "name": "cpu_utilization",
                "host": "prod-server-01",
                "value": 0.85,
                "unit": "percent"
            },
            {
                "name": "memory_usage",
                "host": "prod-server-01",
                "value": 0.72,
                "unit": "percent"
            },
            {
                "name": "disk_space",
                "volume": "/dev/sda1",
                "value": 0.91,
                "unit": "percent"
            }
        ]
    }
    
    # Archive the data
    archive_metrics_to_s3(aws_bucket_name, sample_metrics, region="us-west-2")
