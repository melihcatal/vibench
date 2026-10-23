from google.cloud import vision_v1
import os


def get_vision_client():
    """Returns a Google Cloud Vision API client."""
    return vision_v1.ImageAnnotatorClient()


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
