# speech_client.py
# [HELPER] Local configuration and client helper utilities for Google Cloud Text-to-Speech.

import os
from google.cloud import texttospeech

def get_texttospeech_client() -> texttospeech.TextToSpeechClient:
    """Create and return a reusable TextToSpeechClient using Application Default Credentials.

    The client will pick up credentials from:
    - GOOGLE_APPLICATION_CREDENTIALS environment variable
    - GCE instance metadata
    - Service account key JSON referenced in env var
    - Other ADC sources
    """
    # Ensure credentials are available; otherwise raise helpful error
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS') and not os.getenv('CLOUD_SDK_CONFIG_DIR'):
        raise RuntimeError('Google Application Default Credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS or run `gcloud auth application-default login`.')
    return texttospeech.TextToSpeechClient()
