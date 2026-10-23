from database_client import get_s3_client
import os


def archive_export_to_s3(file_content: bytes, file_name: str, bucket_name: str) -> dict:
    """
    Archives exported document snapshots or attachments in AWS S3 managed object storage.
    """
    s3 = get_s3_client()

    # AWS S3
    response = s3.put_object(
        Bucket=bucket_name,  # AWS S3 bucket_name
        Key=file_name,
        Body=file_content,
    )

    return response
