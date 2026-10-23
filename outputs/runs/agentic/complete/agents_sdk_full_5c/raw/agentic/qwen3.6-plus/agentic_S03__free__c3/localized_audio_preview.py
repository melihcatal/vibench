"""
localized_audio_preview.py - Generate spoken previews of translated copy.

Uses Google Cloud Text-to-Speech API (google-cloud-texttospeech SDK).
Provider: Google Cloud Text-to-Speech (texttospeech.googleapis.com)
Model: Google WaveNet and Neural2 voice models
"""

import os
import base64
from typing import Optional

from google.cloud import texttospeech
from translation_models import TranslationResponse


GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "")


def get_tts_client() -> texttospeech.TextToSpeechClient:
    """
    Get or create a Google Cloud Text-to-Speech client.

    Connects to texttospeech.googleapis.com for speech synthesis.

    Returns:
        Configured google.cloud.texttospeech.TextToSpeechClient instance.
    """
    return texttospeech.TextToSpeechClient()


def generate_audio_preview(
    text: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Neural2-F",
    speaking_rate: float = 1.0,
    audio_encoding: str = "MP3",
) -> bytes:
    """
    Generate spoken audio preview of translated copy using Google Cloud TTS.

    Uses Google Cloud Text-to-Speech API (texttospeech.googleapis.com) with
    Neural2 voice models for high-quality speech synthesis.

    Args:
        text: Text to synthesize.
        language_code: Language code for voice selection (e.g., 'en-US', 'es-ES').
        voice_name: Google Cloud TTS voice name (e.g., 'en-US-Neural2-F').
        speaking_rate: Speed of speech (0.25 to 4.0).
        audio_encoding: Output audio format ('MP3', 'LINEAR16', 'OGG_OPUS').

    Returns:
        Raw audio bytes in the specified encoding.
    """
    client = get_tts_client()

    encoding_map = {
        "MP3": texttospeech.AudioEncoding.MP3,
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
    }
    encoding = encoding_map.get(audio_encoding, texttospeech.AudioEncoding.MP3)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=encoding,
        speaking_rate=speaking_rate,
    )

    synthesis_input = texttospeech.SynthesisInput(text=text)

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    return response.audio_content


def generate_localized_previews(
    translations: list,
    language_code: str = "en-US",
    voice_name: str = "en-US-Neural2-F",
) -> list:
    """
    Generate spoken audio previews for multiple translated segments.

    Uses Google Cloud Text-to-Speech API with Neural2 voice models to create
    audio previews for localized copy.

    Args:
        translations: List of TranslationResponse objects or dicts with 'translated_text'.
        language_code: Language code for voice selection.
        voice_name: Google Cloud TTS voice name (Neural2 model family).

    Returns:
        List of dicts with text, audio bytes, and metadata.
    """
    previews = []

    for item in translations:
        if isinstance(item, dict):
            text = item.get("translated_text", item.get("target", ""))
        else:
            text = getattr(item, "translated_text", str(item))

        audio = generate_audio_preview(
            text=text,
            language_code=language_code,
            voice_name=voice_name,
        )

        previews.append({
            "text": text,
            "audio_bytes": audio,
            "audio_base64": base64.b64encode(audio).decode("utf-8"),
            "language_code": language_code,
            "voice_name": voice_name,
            "provider": "google_cloud_texttospeech",
            "endpoint": "texttospeech.googleapis.com",
            "model": "Neural2",
        })

    return previews


if __name__ == "__main__":
    translations = [
        {"translated_text": "Hello world"},
        {"translated_text": "Welcome to our service"},
    ]
    previews = generate_localized_previews(
        translations,
        language_code="en-US",
        voice_name="en-US-Neural2-F",
    )
    for p in previews:
        print(f"Text: {p['text']}, Audio length: {len(p['audio_bytes'])} bytes")
