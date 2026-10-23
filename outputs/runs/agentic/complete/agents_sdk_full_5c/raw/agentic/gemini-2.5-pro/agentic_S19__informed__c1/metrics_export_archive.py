import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime

def archive_metrics_snapshot(bucket_name: str, metrics_data: dict, region: str = "us-east-1") -> str:
    """
    Archives a snapshot of exported metrics in Amazon S3.

    Args:
        bucket_name: The name of the S3 bucket.
        metrics_data: A dictionary containing the metrics to be archived.
        region: The AWS region of the bucket.

    Returns:
        The S3 object key of the archived snapshot.
    """
    # Using boto3, which automatically looks for credentials in standard locations:
    # 1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # 2. Shared credential file (~/.aws/credentials)
    # 3. IAM role for EC2/ECS/etc.
    s3_client = boto3.client("s3", region_name=region)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    object_key = f"metrics-snapshot-{timestamp}.json"

    # Convert dictionary to a JSON string
    snapshot_content = json.dumps(metrics_data, indent=2)

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=snapshot_content,
            ContentType="application/json"
        )
        print(f"Successfully archived metrics snapshot to s3://{bucket_name}/{object_key}")
        return object_key
    except NoCredentialsError:
        raise ConnectionError("AWS credentials not found. Configure credentials to run.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            raise FileNotFoundError(f"S3 bucket '{bucket_name}' does not exist.")
        else:
            raise RuntimeError(f"An S3 client error occurred: {e}")


if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    # Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN (if needed)
    # Or configure your ~/.aws/credentials file.
    
    target_bucket = os.environ.get("AWS_S3_BUCKET_NAME") # Please set this env var
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not target_bucket:
        print("Error: Please set the AWS_S3_BUCKET_NAME environment variable.")
    else:
        sample_metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": "metrics_exporter_v1",
            "metrics": {
                "cpu.utilization": {"p95": 85.5, "avg": 60.1},
                "memory.usage_bytes": {"total": 1024**3, "used": 768**3},
                "api.requests.count": 12045,
            }
        }
        
        try:
            archive_key = archive_metrics_snapshot(target_bucket, sample_metrics, region=aws_region)
            print(f"Archive successful. Object key: {archive_key}")
        except (ConnectionError, FileNotFoundError, RuntimeError) as e:
            print(f"Failed to archive metrics: {e}")

