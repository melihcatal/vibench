from database_client import get_s3_client
import os
from typing import Optional


def archive_document_snapshot(
    file_content: bytes, bucket_name: str, object_key: str
) -> Optional[str]:
    """
    Archives exported document snapshots or attachments in AWS S3 managed object storage.

    Args:
        file_content: The binary content of the file to archive.
        bucket_name: The name of the S3 bucket to upload to.
        object_key: The key (path) for the object in the S3 bucket.

    Returns:
        The URL of the archived object if successful, otherwise None.
    """
    s3_client = get_s3_client()

    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
        # Construct the URL for the uploaded object
        region = os.getenv("AWS_REGION", "us-east-1")
        object_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
        return object_url

    except Exception as e:
        print(f"Error archiving document snapshot to S3: {e}")
        return None
