import os
from google.cloud import translate_v2 as translate

def get_translate_client():
    """Initializes and returns a Google Cloud Translation client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, you might set it like:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    return translate.Client()
