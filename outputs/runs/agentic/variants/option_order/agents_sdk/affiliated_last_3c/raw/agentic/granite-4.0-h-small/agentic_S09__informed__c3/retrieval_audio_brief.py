import os
from elevenlabs import ElevenLabsClient

def generate_audio_brief(text: str, api_key: str) -> bytes:
    """Create a spoken brief from retrieved search result text using ElevenLabs TTS.

    Args:
        text (str): The text to be spoken.
        api_key (str): ElevenLabs API key.

    Returns:
        bytes: Audio file (in MP3 format) as raw bytes.
    """
    client = ElevenLabsClient(api_key=api_key)
    response = client.generate_speech(
        text=text,
        voice_id="1"
    )
    return response.audio_content
