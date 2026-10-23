import os
import boto3
from google.cloud import documentai_v1 as documentai


def get_documentai_client():
    """Returns a Document AI client."""
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    location = os.getenv("GOOGLE_LOCATION", "us")

    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set.")

    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client, project_id, location


def get_textract_client():
    """Returns a Textract client."""
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region_name = os.getenv("AWS_REGION_NAME", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials are not configured properly.")

    return boto3.client(
        "textract",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region_name,
    )
