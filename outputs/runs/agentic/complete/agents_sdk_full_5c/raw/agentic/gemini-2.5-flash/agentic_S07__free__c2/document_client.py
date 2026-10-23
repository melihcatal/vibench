import os
from google.cloud import documentai_v1 as documentai

def get_documentai_client():
    """Initializes and returns a Google Cloud Document AI client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # For local development, set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
    return documentai.DocumentProcessorServiceClient()

def get_project_id():
    """Gets the Google Cloud project ID from the environment."""
    # This assumes `gcloud config get-value project` or GOOGLE_CLOUD_PROJECT env var is set.
    # In a real application, you might get this from explicit configuration or other environment variables.
    return os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", "your-gcp-project-id"))

def get_location():
    """Gets the Google Cloud location from the environment (e.g., "us")."""
    return os.getenv("GCP_LOCATION", "us")
