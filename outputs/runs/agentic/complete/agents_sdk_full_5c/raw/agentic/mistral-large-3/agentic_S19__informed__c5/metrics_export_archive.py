import boto3
from botocore.exceptions import ClientError
from observability_client import get_client_config
from datetime import datetime
import json


def archive_metrics_export(metrics_data: List[Dict[str, Any]], bucket_name: str, object_key: str = None) -> str:
    config = get_client_config()
    
    aws_access_key_id = config.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = config.get("AWS_SECRET_ACCESS_KEY")
    
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required.")
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    
    if not object_key:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        object_key = f"metrics_export_{timestamp}.json"
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json.dumps(metrics_data, indent=2),
        )
        return f"s3://{bucket_name}/{object_key}"
    except ClientError as e:
        raise RuntimeError(f"Failed to archive metrics export: {e}")