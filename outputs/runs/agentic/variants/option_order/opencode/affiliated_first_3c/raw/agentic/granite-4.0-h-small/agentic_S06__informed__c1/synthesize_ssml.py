import os
from speech_client import TextToSpeechClient


def synthesize_ssml(ssml: str, voice_name: str = None) -> bytes:
    """Synthesize SSML with optional voice and prosody controls using the configured TTS provider.

    Args:
        ssml (str): The SSML markup to convert.
        voice_name (str, optional): Specific voice identifier.

    Returns:
        bytes: The synthesized speech as an audio byte stream (default is WAV format).
    """
    client = TextToSpeechClient()
    response = client.synthesize_ssml(
        input_ssml=ssml,
        voice_name=voice_name,
    )
    return response.audio_content
