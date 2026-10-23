import os
import boto3
from botocore.exceptions import ClientError
from typing import List, Dict


def metrics_export_archive(bucket_name: str, object_key: str, data: List[Dict]) -> str:
    """Archive exported metric snapshots in Amazon S3."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    import json
    json_data = json.dumps(data, indent=2)
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_data,
            ContentType="application/json"
        )
        return f"s3://{bucket_name}/{object_key}"
    except ClientError as e:
        raise Exception(f"Failed to archive metrics: {e}")