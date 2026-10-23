import os
from typing import Optional
from google.cloud import texttospeech
from model_models import AudioRequest, AudioResponse


def generate_audio_brief(request: AudioRequest) -> AudioResponse:
    """Generate spoken briefings from model outputs using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.voice.split("-")[0],
        name=request.voice,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    
    return AudioResponse(audio_content=response.audio_content)