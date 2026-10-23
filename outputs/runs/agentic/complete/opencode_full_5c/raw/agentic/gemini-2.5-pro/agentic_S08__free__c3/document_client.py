import os
from google.cloud import documentai_v1 as documentai


def get_documentai_client():
    """
    Initializes and returns a Document AI client.
    Expects Google Cloud credentials to be configured in the environment.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., 'us' or 'eu'

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client
