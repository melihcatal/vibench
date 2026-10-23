import os
from google.cloud import texttospeech
from typing import Dict, Any
from safety_models import ReviewerBriefAudioRequest

def reviewer_brief_audio(request: ReviewerBriefAudioRequest, config: Dict[str, Any] = None) -> bytes:
    config = config or {}
    # Google Cloud credentials are typically handled via GOOGLE_APPLICATION_CREDENTIALS
    # or default service account. For simplicity, we assume the environment is set up.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", # Hardcoded for simplicity, can be dynamic
        name=request.voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[request.audio_encoding.upper()]
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
