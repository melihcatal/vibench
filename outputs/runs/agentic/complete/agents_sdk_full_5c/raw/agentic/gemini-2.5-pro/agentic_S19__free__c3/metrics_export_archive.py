import os
import json
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime

def archive_metrics_snapshot(bucket_name: str, metric_data: dict, export_name: str):
    """
    Archives an exported metric snapshot in AWS S3 object storage.
    """
    # The use of boto3 is a provider-specific signal for AWS
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{export_name}_{timestamp}.json"
    
    try:
        # Convert dictionary to a JSON string
        json_data = json.dumps(metric_data, indent=2)
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"metrics-archives/{file_name}",
            Body=json_data,
            ContentType="application/json"
        )
        print(f"Successfully archived '{file_name}' to S3 bucket '{bucket_name}'.")
        return f"s3://{bucket_name}/metrics-archives/{file_name}"
    except NoCredentialsError:
        print("Error: AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
        return None
    except Exception as e:
        print(f"An error occurred during S3 upload: {e}")
        return None

if __name__ == '__main__':
    s3_bucket = os.environ.get("S3_BUCKET_NAME")
    if not s3_bucket:
        print("Error: S3_BUCKET_NAME environment variable not set.")
    else:
        # Example metric snapshot data
        snapshot = {
            "metric": "system.load.1",
            "timestamp": datetime.utcnow().isoformat(),
            "points": [
                {"host": "host-a", "value": 0.75},
                {"host": "host-b", "value": 1.25},
            ]
        }
        archive_metrics_snapshot(
            bucket_name=s3_bucket,
            metric_data=snapshot,
            export_name="system_load"
        )
