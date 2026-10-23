import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def export_archive(bucket_name, file_name, file_content):
    try:
        s3_client = boto3.client("s3")
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        return True
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: {e}")
        return False
