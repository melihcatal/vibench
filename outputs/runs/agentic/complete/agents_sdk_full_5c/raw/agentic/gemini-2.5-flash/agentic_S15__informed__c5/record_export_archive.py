import os
import boto3
from typing import Union

def record_export_archive(bucket_name: str, object_key: str, file_path: Union[str, bytes]) -> dict:
    """
    Archive exported document snapshots or attachments in managed object storage (Amazon S3).
    """
    s3_client = boto3.client(
        "s3",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    if isinstance(file_path, str):
        # Assuming file_path is a path to a local file
        s3_client.upload_file(file_path, bucket_name, object_key)
    elif isinstance(file_path, bytes):
        # Assuming file_path is the content in bytes
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_path)
    else:
        raise TypeError("file_path must be a string (file path) or bytes (file content).")

    # You might want to return the S3 object URL or other relevant info
    return {
        "bucket": bucket_name,
        "key": object_key,
        "s3_url": f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    }
