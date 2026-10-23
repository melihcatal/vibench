import os
from google.cloud import documentai


def get_documentai_client():
    """
    Initializes and returns a Document AI client.
    Expects GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us")  # e.g., 'us' or 'eu'

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    return client, project_id, location
