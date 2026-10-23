import os
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account


def get_document_client() -> documentai.DocumentProcessorServiceClient:
    """Initialize and return a Google Document AI client."""
    credentials_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "credentials/google-credentials.json"
    )
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    return documentai.DocumentProcessorServiceClient(credentials=credentials)