import os
from google.cloud import translate_v2 as translate

# Using google-cloud-translate library which uses GOOGLE_APPLICATION_CREDENTIALS
# environment variable for authentication.

_CLIENT = None

def get_translation_client() -> translate.Client:
    """
    Initializes and returns a thread-safe Google Cloud Translation client.
    """
    global _CLIENT
    if _CLIENT is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        _CLIENT = translate.Client(target_language="en")
    return _CLIENT
