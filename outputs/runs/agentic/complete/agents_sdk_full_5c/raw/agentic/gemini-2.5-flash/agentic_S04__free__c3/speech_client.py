from google.cloud import speech_v1p1beta1 as speech
from google.api_core.client_options import ClientOptions
import os

def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # client_options = ClientOptions(api_endpoint="us-speech.googleapis.com") # Example for specific endpoint
    return speech.SpeechClient()

def get_operation_client():
    """Returns a Google Cloud Operation client for polling."""
    return speech.SpeechClient() # SpeechClient also has methods to get operations
