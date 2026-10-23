from google.cloud import translate_v3
import os

# Set your Google Cloud Project ID and Location
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv(
    "GOOGLE_CLOUD_LOCATION", "global"
)  # Or a specific region like "us-central1"


def get_translation_client():
    """Returns a Google Cloud Translation V3 client."""
    return translate_v3.TranslationServiceClient()
