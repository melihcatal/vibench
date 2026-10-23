# [SAME-SCENARIO] synthesize_text.py

import os
from typing import Optional
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient
from .speech_models import SynthesisInput, AudioConfig, VoiceSelectionParams

def synthesize_text(
    client: TextToSpeechClient,
    text: str,
    voice: Optional[str] = None,
    audio_encoding: str = "MP3",
) -> bytes:
    """Synthesize plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        client: Configured TextToSpeechClient.
        text: Plain text to synthesize.
        voice: Optional BCP-47 language tag (e.g., "en-US"). If None, client default is used.
        audio_encoding: Encoding format for the output audio.

    Returns:
        Audio content as bytes.
    """
    input_data = SynthesisInput(text=text)
    # Select voice if provided, otherwise fall back to client's default_voice.
    selected_voice = voice if voice else client.default_voice
    voice_params = VoiceSelectionParams(
        language_code=selected_voice.split('-')[0],
        name=selected_voice,
    )
    config = AudioConfig(audio_encoding=audio_encoding)
    response = client.client.synthesize_speech(
        input=input_data, voice=voice_params, audio_config=config
    )
    return response.audio_content
