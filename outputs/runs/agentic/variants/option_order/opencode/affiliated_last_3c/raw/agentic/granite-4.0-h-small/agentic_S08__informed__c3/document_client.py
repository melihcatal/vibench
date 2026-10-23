# [HELPER] document_client.py
# Local configuration and client utilities for Structured Document Extraction

import os

# AWS credentials for Textract
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Azure endpoint/key for Document Intelligence
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# Mindee API key for invoice OCR
MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")

# Function utilities


def get_textract_client():
    """Create a Textract client using environment variables."""
    return boto3.client(
        "textract",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def get_minede_client():
    """Return a configured Mindee client."""
    return mindee.Client(api_key=MINDEE_API_KEY)
