import boto3
from database_client import get_s3_client

def export_archive(bucket_name, file_name, file_content):
    s3 = get_s3_client()
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=file_content
    )