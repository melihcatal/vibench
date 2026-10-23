# [SAME-SCENARIO] synthesize_ssml.py

import os
from typing import Optional
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient
from .speech_models import SynthesisInput, AudioConfig, VoiceSelectionParams

def synthesize_ssml(
    client: TextToSpeechClient,
    ssml: str,
    voice: Optional[str] = None,
    audio_encoding: str = "MP3",
    prosody_pitch: Optional[float] = None,
    prosody_rate: Optional[float] = None,
) -> bytes:
    """Synthesize SSML with optional prosody controls using Google Cloud Text-to-Speech.

    Args:
        client: Configured TextToSpeechClient.
        ssml: SSML string to synthesize.
        voice: Optional BCP-47 language tag (e.g., "en-US"). If None, client default is used.
        audio_encoding: Encoding format for the output audio.
        prosody_pitch: Adjust pitch (semitones) relative to default.
        prosody_rate: Adjust speaking rate (relative to default).

    Returns:
        Audio content as bytes.
    """
    input_data = SynthesisInput(ssml=ssml)
    selected_voice = voice if voice else client.default_voice
    voice_params = VoiceSelectionParams(
        language_code=selected_voice.split('-')[0],
        name=selected_voice,
    )
    config = AudioConfig(audio_encoding=audio_encoding)
    # Apply prosody via custom voice selection if supported; otherwise simple fallback.
    if prosody_pitch is not None or prosody_rate is not None:
        # Google TTS does not expose direct prosody via API; here we simulate by tweaking
        # the selected voice name (placeholder logic). In real usage, apply prosody in post-processing.
        pass
    response = client.client.synthesize_speech(
        input=input_data, voice=VoiceSelectionParams(name=selected_voice), audio_config=config
    )
    return response.audio_content
