import os
from google.cloud import texttospeech
from typing import Dict, Any
import base64


def generate_spoken_preview(
    text: str, language_code: str = "en-US", voice_name: str = None
) -> Dict[str, Any]:
    """Generate spoken previews of translated copy using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice_config = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    if voice_name:
        voice_config.name = voice_name

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_config, audio_config=audio_config
    )

    audio_content = response.audio_content
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")

    return {
        "text": text,
        "language_code": language_code,
        "voice_name": voice_config.name
        if voice_name
        else f"Standard {language_code} voice",
        "audio_encoding": "MP3",
        "audio_content_base64": audio_base64,
        "audio_size_bytes": len(audio_content),
        "provider": "Google Cloud Text-to-Speech",
    }


def get_available_voices(language_code: str = None) -> Dict[str, Any]:
    """Get available voices for text-to-speech."""
    client = texttospeech.TextToSpeechClient()

    voices = client.list_voices(language_code=language_code)

    voice_list = []
    for voice in voices.voices:
        voice_list.append(
            {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )

    return {
        "voices": voice_list,
        "total_count": len(voice_list),
        "language_filter": language_code,
    }
