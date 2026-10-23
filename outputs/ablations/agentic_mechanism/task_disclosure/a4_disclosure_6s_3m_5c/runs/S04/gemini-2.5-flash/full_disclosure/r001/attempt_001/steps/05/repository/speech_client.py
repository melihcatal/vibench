import os
from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    """
    Provides a client for Google Cloud Batch Speech-to-Text.

    Returns:
        google.cloud.speech_v1p1beta1.SpeechClient: A Google Cloud Speech-to-Text client.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate via other methods supported by google-cloud-python.
    # For local development, setting GOOGLE_APPLICATION_CREDENTIALS to the path of your
    # service account key file is common.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    client = speech.SpeechClient()
    return client

def get_project_id():
    """
    Retrieves the Google Cloud Project ID from the environment variable.

    Returns:
        str: The Google Cloud Project ID.
    Raises:
        ValueError: If GOOGLE_CLOUD_PROJECT environment variable is not set.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Environment variable GOOGLE_CLOUD_PROJECT not set.")
    return project_id
