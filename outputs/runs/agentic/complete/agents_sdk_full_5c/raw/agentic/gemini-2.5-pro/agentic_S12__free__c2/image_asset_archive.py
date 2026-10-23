import os
import boto3
from vision_client import (
    B2_ENDPOINT_URL,
    B2_ACCESS_KEY_ID,
    B2_SECRET_ACCESS_KEY,
)
from vision_models import ArchiveResult

def archive_assets(bucket_name: str, object_name: str, data_bytes: bytes) -> ArchiveResult:
    """
    Archives image analysis artifacts to Backblaze B2 cloud storage.
    """
    if not all([B2_ENDPOINT_URL, B2_ACCESS_KEY_ID, B2_SECRET_ACCESS_KEY]):
        raise ValueError("Backblaze B2 credentials are not fully configured.")

    s3_client = boto3.client(
        service_name="s3",
        endpoint_url=B2_ENDPOINT_URL,
        aws_access_key_id=B2_ACCESS_KEY_ID,
        aws_secret_access_key=B2_SECRET_ACCESS_KEY,
    )

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=data_bytes,
        ContentType='application/json; charset=utf-8'
    )
    
    # Note: Backblaze B2 public URLs can have different formats.
    # This is a common format but might need adjustment based on bucket settings.
    # Example: https://f005.backblazeb2.com/file/your-bucket-name/your-object-name
    # We will construct a generic one for the example.
    
    # Extract hostname from endpoint for URL construction
    url_base = B2_ENDPOINT_URL.replace(f"s3.{B2_ENDPOINT_URL.split('.')[1]}.backblazeb2.com", f"f005.backblazeb2.com")

    file_url = f"{url_base}/file/{bucket_name}/{object_name}"

    return ArchiveResult(
        bucket=bucket_name,
        key=object_name,
        url=file_url
    )
