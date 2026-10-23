import os
import boto3
from botocore.exceptions import ClientError

def archive_document(document_id: str, content: bytes) -> str:
    """Archive a document snapshot in Amazon S3."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "document-archive")
    
    object_key = f"documents/{document_id}.json"
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=content)
    
    return f"s3://{bucket_name}/{object_key}"