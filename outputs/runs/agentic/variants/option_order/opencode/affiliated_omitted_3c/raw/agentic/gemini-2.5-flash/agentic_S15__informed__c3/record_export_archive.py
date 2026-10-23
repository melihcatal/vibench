import os
from database_client import get_s3_client


def archive_document_snapshot(bucket_name: str, file_name: str, file_content: bytes):
    s3_client = get_s3_client()
    response = s3_client.put_object(
        Bucket=bucket_name, Key=file_name, Body=file_content
    )
    return response
