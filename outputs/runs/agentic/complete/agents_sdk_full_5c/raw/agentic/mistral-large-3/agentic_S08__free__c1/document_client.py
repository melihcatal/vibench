import os
from google.cloud import documentai_v1 as documentai
import boto3


def get_document_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )


def get_textract_client():
    return boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )