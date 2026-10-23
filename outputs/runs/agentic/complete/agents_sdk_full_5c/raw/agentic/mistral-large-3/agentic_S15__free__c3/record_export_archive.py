import os
from typing import Dict, Any, List
import boto3
from botocore.exceptions import NoCredentialsError
from database_models import DocumentResponse

# Initialize AWS S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "<your-access-key>"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "<your-secret-key>")
)

def export_document_to_s3(document: DocumentResponse, bucket_name: str, object_key: str) -> str:
    """
    Archives a document snapshot to AWS S3 managed object storage.
    
    Args:
        document: The document to archive.
        bucket_name: The S3 bucket name.
        object_key: The S3 object key (path) for the document.
        
    Returns:
        The S3 object URL.
    """
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=str(document.data).encode("utf-8")
    )
    return f"https://{bucket_name}.s3.amazonaws.com/{object_key}"