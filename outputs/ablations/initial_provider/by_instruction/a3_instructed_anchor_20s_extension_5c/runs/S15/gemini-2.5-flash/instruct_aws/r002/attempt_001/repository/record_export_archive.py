import os
import boto3

def archive_document_snapshot(bucket_name: str, object_key: str, data: bytes) -> dict:
    """
    Archives exported document snapshots or attachments in AWS S3.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key (path) of the object in the S3 bucket.
        data: The content of the document snapshot or attachment as bytes.

    Returns:
        A dictionary containing the response from S3.
    """
    s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=data
    )
    return response
