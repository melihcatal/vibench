import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def get_document_client() -> documentai.DocumentProcessorServiceClient:
    client_options = ClientOptions(
        api_endpoint=f"{os.getenv('GCP_LOCATION')}-documentai.googleapis.com"
    )
    return documentai.DocumentProcessorServiceClient(client_options=client_options)


def load_env():
    required_vars = [
        "GCP_PROJECT_ID",
        "GCP_LOCATION",
        "GCP_INVOICE_PROCESSOR_ID",
        "GCP_RECEIPT_PROCESSOR_ID"
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")