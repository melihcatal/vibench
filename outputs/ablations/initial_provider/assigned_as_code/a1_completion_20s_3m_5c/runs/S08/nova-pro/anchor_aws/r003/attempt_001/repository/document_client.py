import os
import boto3


def get_textract_client(region=None):
    region = region or os.getenv("AWS_DEFAULT_REGION", "us-west-2")
    return boto3.client("textract", region_name=region)


def get_document_bytes(file_path):
    with open(file_path, "rb") as file:
        return file.read()