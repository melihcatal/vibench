import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Dict, Any, Optional


def get_s3_client():
    """Initialize and return the Amazon S3 client." ""
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def archive_document(document_id: str, document: Dict[str, Any], bucket_name: Optional[str] = None) -> str:
    """
    Archives a document snapshot in Amazon S3.
    
    Args:
        document_id: The identifier of the document.
        document: The document to archive.
        bucket_name: The S3 bucket name (default: environment variable).
        
    Returns:
        The S3 object URL of the archived document.
    """
    s3_client = get_s3_client()
    bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME", "document-archive-bucket")
    
    object_key = f"documents/{document_id}.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=str(document),
        ContentType="application/json"
    )
    
    return f"s3://{bucket_name}/{object_key}"


def archive_attachment(document_id: str, file_path: str, bucket_name: Optional[str] = None) -> str:
    """
    Archives a document attachment in Amazon S3.
    
    Args:
        document_id: The identifier of the document.
        file_path: The local path to the attachment file.
        bucket_name: The S3 bucket name (default: environment variable).
        
    Returns:
        The S3 object URL of the archived attachment.
    """
    s3_client = get_s3_client()
    bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME", "document-archive-bucket")
    
    object_key = f"attachments/{document_id}/{os.path.basename(file_path)}"
    s3_client.upload_file(file_path, bucket_name, object_key)
    
    return f"s3://{bucket_name}/{object_key}"