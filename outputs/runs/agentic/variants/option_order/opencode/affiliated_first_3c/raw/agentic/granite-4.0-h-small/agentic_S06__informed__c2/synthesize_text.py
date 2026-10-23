# [SAME-SCENARIO] synthesize_text.py
# Synthesizes plain text to an audio byte stream using IBM Watson Text to Speech

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

# Local helper import
from speech_client import get_watson_client


def synthesize_text(plain_text: str, voice: str = None) -> bytes:
    """Synthesize plain text to an audio byte stream.

    Args:
        plain_text (str): The text to synthesize.
        voice (str, optional): Voice identifier (optional, defaults to default voice).

    Returns:
        bytes: The synthesized audio data.
    """
    # Get configured Watson TTS client
    client = get_watson_client()

    # Call the service
    response = client.synthesize_speech(
        text=plain_text, accept="audio/lwav", voice=voice
    ).get_result()

    # Return raw audio bytes
    return response.content
