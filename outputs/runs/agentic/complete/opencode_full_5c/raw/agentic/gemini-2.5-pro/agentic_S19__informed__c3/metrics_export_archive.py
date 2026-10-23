import os
import boto3
from botocore.exceptions import ClientError
import json
from typing import List, Dict, Any


def archive_metrics_to_s3(
    bucket_name: str, object_key: str, metric_data: List[Dict[str, Any]]
) -> bool:
    """
    Archives a snapshot of metric data to an Amazon S3 bucket.
    """
    # Authentication is handled by boto3 via environment variables like
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN.
    s3_client = boto3.client("s3")

    try:
        # Convert metric data to a JSON string
        data_to_upload = json.dumps(metric_data, indent=2)

        # The put_object method uploads data to the specified S3 bucket.
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=data_to_upload,
            ContentType="application/json",
        )
        return True
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
