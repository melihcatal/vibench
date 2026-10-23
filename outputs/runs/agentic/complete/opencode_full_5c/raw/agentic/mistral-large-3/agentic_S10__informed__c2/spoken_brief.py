import os
from typing import Optional

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def generate_spoken_brief(
    text: str,
    voice: str = "en-US_AllisonV3Voice",
    accept: str = "audio/wav",
) -> bytes:
    """
    Generate a spoken brief from the model output using Watson Text to Speech.
    """
    api_key = os.getenv("IBM_TTS_APIKEY")
    url = os.getenv("IBM_TTS_URL")

    if not api_key or not url:
        raise ValueError("IBM TTS credentials not set in environment variables")

    authenticator = IAMAuthenticator(api_key)
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(url)

    response = client.synthesize(
        text,
        voice=voice,
        accept=accept,
    ).get_result()

    return response.content
