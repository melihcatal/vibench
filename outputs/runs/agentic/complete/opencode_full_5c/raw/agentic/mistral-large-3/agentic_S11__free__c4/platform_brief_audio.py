import os
from typing import Dict, Any
from google.cloud import texttospeech

from .model_models import ChatResponse


def platform_brief_audio(
    response: ChatResponse,
    output_file: str = "output.mp3",
    language_code: str = "en-US",
    voice_name: str = "en-US-Wavenet-D",
) -> Dict[str, Any]:
    """
    Generates spoken briefings from Azure AI Inference model outputs using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=response.content)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    return {
        "output_file": output_file,
        "voice_name": voice_name,
        "language_code": language_code,
        "provider": "google_cloud_text_to_speech",
    }
