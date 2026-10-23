# [SAME-SCENARIO] synthesize_ssml.py

import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()


def synthesize_ssml(
    ssml: str, voice_name: str = None, audio_format: str = "MP3"
) -> bytes:
    """Synthesizes SSML to an audio byte stream using Google Cloud TTS.

    Args:
        ssml: The SSML string to synthesize.
        voice_name: Optional voice name (e.g., "en-US-Standard-C").
        audio_format: Output audio format ("MP3", "LINEAR16").

    Returns:
        Bytes of the synthesized audio.
    """
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_format)
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return response.audio_content
