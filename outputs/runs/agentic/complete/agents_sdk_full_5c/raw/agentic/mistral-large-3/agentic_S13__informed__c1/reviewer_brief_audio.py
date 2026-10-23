import os
from typing import Dict, Any
from google.cloud import texttospeech_v1 as tts


def generate_reviewer_brief(text: str, language_code: str = "en-US") -> bytes:
    """Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech."""
    client = tts.TextToSpeechClient()

    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code=language_code,
        name="en-US-Wavenet-D"
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content