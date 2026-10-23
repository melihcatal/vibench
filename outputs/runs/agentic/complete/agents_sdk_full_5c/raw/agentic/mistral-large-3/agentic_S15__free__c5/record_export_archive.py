import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError

def archive_document_snapshot(document: Dict[str, Any], bucket_name: str, object_key: str) -> str:
    """
    Archives a document snapshot in Amazon S3 managed object storage.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=str(document).encode('utf-8')
        )
        return f"s3://{bucket_name}/{object_key}"
    except ClientError as e:
        raise Exception(f"Failed to archive document: {e}")