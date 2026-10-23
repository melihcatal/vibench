import os
from google.cloud import documentai
from google.api_core.client_options import ClientOptions


def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    """
    Initializes and returns a Document AI client.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client
