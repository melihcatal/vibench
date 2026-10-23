import os
import boto3
from botocore.exceptions import ClientError
import json
from typing import List, Dict, Any

def archive_metrics_to_s3(
    bucket_name: str, 
    object_name: str, 
    metric_data: List[Dict[str, Any]]
) -> bool:
    """
    Archives exported metric snapshots in Amazon S3.
    Assumes AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are in the environment.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The key for the new object in S3 (e.g., 'exports/metrics-2023-10-27.json').
    :param metric_data: The metric data to serialize and upload.
    :return: True if the upload was successful, False otherwise.
    """
    s3_client = boto3.client("s3")

    # Serialize the metric data to a JSON string
    data_str = json.dumps(metric_data, indent=2)
    data_bytes = data_str.encode("utf-8")

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=data_bytes,
            ContentType='application/json'
        )
        print(f"Successfully uploaded {object_name} to {bucket_name}")
        return True
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
