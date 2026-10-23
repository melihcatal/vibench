from typing import Dict, Optional
import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def reviewer_brief_audio(
    text: str,
    voice: str = "en-US_AllisonV3Voice",
    output_format: str = "audio/mp3",
) -> bytes:
    """
    Generate spoken briefs for moderation reviewers using Watson Text to Speech.
    """
    api_key = os.getenv("IBM_TTS_APIKEY")
    url = os.getenv("IBM_TTS_URL")

    if not api_key or not url:
        raise ValueError("Watson Text to Speech credentials not configured")

    authenticator = IAMAuthenticator(api_key)
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(url)

    response = client.synthesize(
        text,
        voice=voice,
        accept=output_format,
    ).get_result()

    return response.content
