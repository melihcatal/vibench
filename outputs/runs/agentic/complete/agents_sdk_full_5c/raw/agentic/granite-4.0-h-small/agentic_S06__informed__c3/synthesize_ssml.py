import os
from speech_client import get_text_to_speech_client
from speech_models import OutputFormat

def synthesize_ssml(ssml: str, voice: str, locale: str, format: OutputFormat = OutputFormat.WAV) -> bytes:
    """Synthesize SSML with voice, prosody and speaking rate controls using Azure Speech TTS.
    Returns the audio data as bytes.
    """
    client = get_text_to_speech_client()
    response = client.synthesize_speech(
        text=ssml,
        voice_name=voice,
        voice_config={"locale": locale},
        ssml=True,
        output_format=format
    )
    return response.audio_content
