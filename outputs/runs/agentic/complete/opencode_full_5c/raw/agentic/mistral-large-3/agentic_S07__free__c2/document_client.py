import os
from typing import Optional
from google.cloud import vision_v1, documentai_v1
from google.oauth2 import service_account


def get_document_client() -> vision_v1.ImageAnnotatorClient:
    """Initialize and return Google Cloud Vision client."""
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
    )
    return vision_v1.ImageAnnotatorClient(credentials=credentials)


def get_document_processor_client() -> documentai_v1.DocumentProcessorServiceClient:
    """Initialize and return Google Cloud Document AI client."""
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
    )
    return documentai_v1.DocumentProcessorServiceClient(credentials=credentials)
