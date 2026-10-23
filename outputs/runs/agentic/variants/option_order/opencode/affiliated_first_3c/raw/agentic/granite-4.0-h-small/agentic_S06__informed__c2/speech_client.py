# [HELPER] speech_client.py
# Local configuration and client helper utilities for Text-to-Speech

import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1


def get_watson_client() -> TextToSpeechV1:
    """Instantiate and return a configured Watson Text-to-Speech client.

    Uses IBM Cloud API key and service URL from environment variables.
    """
    api_key = os.getenv("IBM_TTS_APIKEY")
    url = os.getenv("IBM_TTS_URL")
    if not api_key:
        raise RuntimeError("IBM_TTS_APIKEY not set")
    if not url:
        raise RuntimeError("IBM_TTS_URL not set")
    authenticator = IAMAuthenticator(api_key)
    return TextToSpeechV1(authenticator=authenticator, service_url=url)


# Placeholder for other providers
# def get_azure_client(): ...
# def get_google_client(): ...
# Add similar helpers when multiple providers are supported.
