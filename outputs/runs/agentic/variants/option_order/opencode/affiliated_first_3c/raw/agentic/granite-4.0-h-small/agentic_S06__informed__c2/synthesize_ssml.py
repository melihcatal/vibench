# [SAME-SCENARIO] synthesize_ssml.py
# Synthesizes SSML with voice and prosody controls using IBM Watson Text to Speech

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

# Local helper import
from speech_client import get_watson_client


def synthesize_ssml(ssml: str, voice: str = None) -> bytes:
    """Synthesize SSML to an audio byte stream.

    Args:
        ssml (str): The SSML markup to synthesize.
        voice (str, optional): Voice identifier (optional, defaults to default voice).

    Returns:
        bytes: The synthesized audio data.
    """
    client = get_watson_client()
    response = client.synthesize_speech(
        text=ssml, accept="audio/lwav", voice=voice, content_type="application/ssml+xml"
    ).get_result()
    return response.content
