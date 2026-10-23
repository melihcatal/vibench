import os
from google.cloud import documentai_v1beta3 as documentai


def get_document_ai_client(type: str = "invoice"):
    """
    Helper to instantiate a Document AI client.
    Authenticates using GOOGLE_APPLICATION_CREDENTIALS env var.
    type can be 'invoice' or 'receipt' to select different processors.
    Returns a DocumentProcessorServiceClient.
    """
    client = documentai.DocumentProcessorServiceClient()
    return client
