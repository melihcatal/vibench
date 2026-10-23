import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError


def archive_document(document: Dict[str, Any], archive_name: str) -> bool:
    s3 = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    bucket_name = os.getenv("AWS_S3_ARCHIVE_BUCKET", "document-archives")
    
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=f"{archive_name}/{document['document_id']}.json",
            Body=str(document),
            ContentType="application/json"
        )
        return True
    except ClientError as e:
        print(f"Error archiving document: {e}")
        return False