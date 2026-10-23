import os
import io
import json
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient
from .speech_models import SynthesisInput, SSMLInput, VoiceSelectionParams, AudioConfig

def synthesize_ssml(ssml: str, voice_name: str = None, language_code: str = 'en-US', prosody_strength: str = 'medium') -> bytes:
    """Synthesize SSML to an audio byte stream using Google Cloud TTS.

    Returns the audio data as a bytes object.
    """
    client = TextToSpeechClient()
    input_data = SSMLInput(ssml=ssml)
    if voice_name:
        voice = client.get_voice_by_name(voice_name)
    else:
        voice = client.select_default_voice(language_code)
    audio = AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
        pitch=0.0,
        prosody_strength=prosody_strength
    )
    response = client.synthesize_speech(input=input_data, voice=voice, audio_config=audio)
    return response.audio_content
