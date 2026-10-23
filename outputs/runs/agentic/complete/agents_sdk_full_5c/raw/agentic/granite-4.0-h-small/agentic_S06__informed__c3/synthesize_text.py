import os
from speech_client import get_text_to_speech_client
from speech_models import OutputFormat

def synthesize_text(text: str, voice: str, locale: str, format: OutputFormat = OutputFormat.WAV) -> bytes:
    """Synthesize plain text to an audio byte stream using Azure Speech TTS.
    Returns the audio data as bytes.
    """
    client = get_text_to_speech_client()
    response = client.synthesize_speech(
        text=text,
        voice_name=voice,
        voice_config={"locale": locale},
        output_format=format
    )
    return response.audio_content
