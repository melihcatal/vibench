import os
from google.cloud import documentai_v1 as documentai


def get_documentai_client():
    """Returns a Google Document AI client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    return documentai.DocumentProcessorServiceClient()
