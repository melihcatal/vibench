import os
from speech_client import TextToSpeechClient


def synthesize(
    text: str, voice_name: str = None, language_code: str = "en-US"
) -> bytes:
    """Synthesize plain text to an audio byte stream using the configured TTS provider.

    Args:
        text (str): The text to convert.
        voice_name (str, optional): Specific voice identifier.
        language_code (str, optional): Language of the text.

    Returns:
        bytes: The synthesized speech as an audio byte stream (default is WAV format).
    """
    client = TextToSpeechClient()
    response = client.synthesize_speech(
        input_text=text,
        voice_name=voice_name,
        language_code=language_code,
    )
    return response.audio_content
