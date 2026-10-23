import os
import boto3
from typing import Dict, Any, Union

def image_asset_archive(filename: str, content: Union[bytes, str], metadata: Dict[str, str] = None) -> Dict[str, str]:
    """
    Archives image-analysis artifacts and derived captions in AWS S3 managed object storage.

    Args:
        filename: The name of the file to save in S3.
        content: The content of the file (bytes for images, string for text/json).
        metadata: Optional metadata to associate with the S3 object.

    Returns:
        A dictionary containing the S3 object URL or other confirmation.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    bucket_name = os.environ.get("S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("S3_ARCHIVE_BUCKET environment variable not set.")

    extra_args = {'Metadata': metadata} if metadata else None

    if isinstance(content, bytes):
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=content, **(extra_args or {}))
    else:
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=content.encode('utf-8'), **(extra_args or {}))

    s3_object_url = f"https://{bucket_name}.s3.{os.environ.get('AWS_REGION', 'us-east-1')}.amazonaws.com/{filename}"

    return {"archive_url": s3_object_url}
