from google.cloud import speech_v1p1beta1 as speech
import os

def get_speech_client():
    """
    Returns a configured Google Cloud Speech-to-Text client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    return speech.SpeechClient()

def get_gcs_uri(bucket_name: str, object_name: str) -> str:
    """
    Constructs a Google Cloud Storage URI.
    """
    return f"gs://{bucket_name}/{object_name}"
