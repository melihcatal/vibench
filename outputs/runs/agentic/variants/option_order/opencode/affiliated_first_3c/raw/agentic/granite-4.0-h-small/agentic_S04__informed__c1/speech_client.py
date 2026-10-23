# LOCAL HELPER - Provides configuration and client utilities for Batch Speech-to-Text

import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configuration values loaded from environment variables
IBM_STT_APIKEY = os.getenv("IBM_STT_APIKEY")
IBM_STT_URL = os.getenv(
    "IBM_STT_URL", "https://api.us-south.speech-to-text.watson.cloud.ibm.com"
)

# Create a reusable authenticated client
authenticator = IAMAuthenticator(IBM_STT_APIKEY)
speech_client = SpeechToTextV1(authenticator=authenticator)
speech_client.set_service_url(IBM_STT_URL)


def get_stt_client():
    """Returns the configured IBM Watson Speech-to-Text client."""
    return speech_client
