from typing import Dict, Any
from model_models import ChatResponse
from google.cloud import texttospeech


def platform_brief_audio(response: ChatResponse) -> Dict[str, Any]:
    """
    Generates spoken briefings from Azure AI Inference model output using Google Cloud Text-to-Speech.
    Uses "en-US-Wavenet-D" as the concrete voice model identifier.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=response.content)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    audio_response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    return {
        "audio_content": audio_response.audio_content,
        "mime_type": "audio/mpeg",
        "voice_model": "en-US-Wavenet-D",
    }
