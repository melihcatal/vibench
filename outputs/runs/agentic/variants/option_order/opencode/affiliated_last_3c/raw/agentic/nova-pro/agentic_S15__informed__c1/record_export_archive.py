import os
import boto3
from botocore.exceptions import NoCredentialsError


def record_export_archive(file_path):
    s3 = boto3.client("s3")
    try:
        with open(file_path, "rb") as data:
            s3.upload_fileobj(data, "your-bucket-name", "archived-document.txt")
        return "File uploaded successfully"
    except NoCredentialsError:
        return "No AWS credentials found"
