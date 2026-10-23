# [LATER-STEP] reviewer_brief_audio.py

import os
from typing import Any, Dict

# Using the Watson Text-to-Speech service to generate spoken briefs for moderation reviewers.
# Credentials supplied via IBM_TTS_APIKEY and IBM_TTS_URL environment variables.


def generate_spoken_brief(text: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """Synthesize an audio file (WAV) containing the provided reviewer brief.

    Returns raw WAV bytes suitable for saving or streaming.
    """
    try:
        from ibm_watson import TextToSpeechV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    except ImportError:
        raise RuntimeError(
            "IBM Watson TTS SDK not installed. Run `pip install ibm-watson` to enable TTS."
        )
    apikey = os.getenv("IBM_TTS_APIKEY")
    service_url = os.getenv("IBM_TTS_URL")
    if not apikey or not service_url:
        raise RuntimeError(
            "Environment variables IBM_TTS_APIKEY and IBM_TTS_URL must be set."
        )
    authenticator = IAMAuthenticator(apikey)
    tts = TextToSpeechV1(authenticator=authenticator, service_url=service_url)
    # The TTS SDK expects the voice name; defaults to Michael if omitted.
    response = tts.synthesize(text, accept="audio/wav", voice=voice)
    return response.get_result().content
