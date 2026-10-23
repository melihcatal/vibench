import os
from google.cloud import documentai_v1 as documentai


def get_documentai_client():
    """Returns a Google Document AI client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate via other means supported by google-cloud-python
    return documentai.DocumentProcessorServiceClient()
