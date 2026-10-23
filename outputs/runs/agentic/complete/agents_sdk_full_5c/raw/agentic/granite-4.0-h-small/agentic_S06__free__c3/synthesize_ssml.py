# synthesize_ssml.py
# [SAME-SCENARIO]
# Synthesizes SSML input with voice and prosody controls using Google Cloud Text-to-Speech.

import os
from google.cloud import texttospeech

# Helper utilities from same-scenario local files
from speech_client import TextToSpeechClient
from speech_models import SynthesizeSpeechResponse

def synthesize_ssml(ssml: str, language_code: str = "en-US", voice_name: str = None) -> bytes:
    """Synthesize SSML into an audio byte stream.
    Args:
        ssml: SSML formatted string.
        language_code: BCP-47 language identifier (default en-US).
        voice_name: Optional specific voice ID (e.g., "en-US-Wavenet-D").
    Returns:
        Binary audio data in MP3 format.
    """
    client = TextToSpeechClient()
    if not voice_name:
        voice_name = select_voice(language_code)[0]
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    resp = SynthesizeSpeechResponse(response)
    resp.validate()
    return response.audio_content
