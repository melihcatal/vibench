import os
from typing import Optional
from google.cloud import texttospeech
from pydantic import BaseModel


class AudioBrief(BaseModel):
    audio_content: bytes
    mime_type: str


def generate_audio_brief(text: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-D") -> AudioBrief:
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioBrief(
        audio_content=response.audio_content,
        mime_type="audio/mpeg"
    )