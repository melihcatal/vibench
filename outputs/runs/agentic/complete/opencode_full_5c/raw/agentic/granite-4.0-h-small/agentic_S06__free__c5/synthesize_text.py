# [SAME-SCENARIO] synthesize_text.py

import os
from google.cloud import texttospeech

# Load credentials from env var (ensure GOOGLE_APPLICATION_CREDENTIALS is set)
client = texttospeech.TextToSpeechClient()


def synthesize_text(
    text: str, voice_name: str = None, audio_format: str = "MP3"
) -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud TTS.

    Args:
        text: The plain text to synthesize.
        voice_name: Optional voice name (e.g., "en-US-Standard-C").
        audio_format: Output audio format ("MP3", "LINEAR16", etc.).

    Returns:
        Bytes of the synthesized audio.
    """
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,  # None uses default voice
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
