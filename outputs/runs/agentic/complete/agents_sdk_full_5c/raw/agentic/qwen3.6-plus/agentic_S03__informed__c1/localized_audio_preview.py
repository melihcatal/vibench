"""
Generate spoken previews of translated copy.

Provider: ElevenLabs Text to Speech
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

import io
import os
from typing import Any, Dict, Optional

from elevenlabs import ElevenLabs, Voice
from elevenlabs.client import ElevenLabs as ElevenLabsClient


def generate_audio_preview(
    text: str,
    target_lang: str,
    voice_id: Optional[str] = None,
    voice_name: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Generate a spoken audio preview of translated copy using ElevenLabs.

    Args:
        text: The translated text to convert to speech.
        target_lang: Target language code (e.g., 'en', 'de', 'fr', 'es', 'ja').
        voice_id: Specific ElevenLabs voice ID to use.
        voice_name: Voice name to look up (e.g., 'Rachel', 'Bella').
        model_id: ElevenLabs model identifier (default: eleven_multilingual_v2).
        output_format: Audio output format (e.g., 'mp3_44100_128').
        stability: Voice stability setting (0.0-1.0).
        similarity_boost: Voice similarity boost (0.0-1.0).

    Returns:
        Dictionary containing audio bytes, metadata, and format info.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")

    client = ElevenLabs(api_key=api_key)

    # Resolve voice
    if voice_id:
        voice = Voice(voice_id=voice_id)
    elif voice_name:
        voices = client.voices.get_all()
        voice_id = None
        for v in voices.voices:
            if v.name.lower() == voice_name.lower():
                voice_id = v.voice_id
                break
        if voice_id is None:
            raise ValueError(f"Voice '{voice_name}' not found in ElevenLabs.")
        voice = Voice(voice_id=voice_id)
    else:
        # Default voice
        voice = Voice(voice_id="EXAVITQu4vr4xnSDxMaL")

    # Build voice settings
    voice_settings = {}
    if stability is not None:
        voice_settings["stability"] = stability
    if similarity_boost is not None:
        voice_settings["similarity_boost"] = similarity_boost

    if voice_settings:
        voice.settings = voice_settings

    audio = client.text_to_speech.convert(
        voice_id=voice.voice_id,
        output_format=output_format,
        text=text,
        model_id=model_id,
        voice_settings=voice.settings if voice.settings else None,
    )

    audio_bytes = b"".join(audio)

    return {
        "text": text,
        "target_lang": target_lang,
        "voice_id": voice.voice_id,
        "model_id": model_id,
        "output_format": output_format,
        "audio_bytes": audio_bytes,
        "audio_size_bytes": len(audio_bytes),
    }


def generate_batch_audio_previews(
    translations: Dict[str, str],
    target_lang: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
) -> Dict[str, Dict[str, Any]]:
    """
    Generate audio previews for a dictionary of translated strings.

    Args:
        translations: Dictionary of translated key-value pairs.
        target_lang: Target language code.
        voice_id: ElevenLabs voice ID to use.
        model_id: ElevenLabs model identifier.

    Returns:
        Dictionary mapping original keys to their audio preview data.
    """
    results = {}
    for key, text in translations.items():
        result = generate_audio_preview(
            text=text,
            target_lang=target_lang,
            voice_id=voice_id,
            model_id=model_id,
        )
        results[key] = result
    return results


def generate_audio_preview_to_file(
    text: str,
    target_lang: str,
    output_path: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
) -> str:
    """
    Generate a spoken audio preview and save to file.

    Args:
        text: The translated text to convert to speech.
        target_lang: Target language code.
        output_path: File path to save the audio file.
        voice_id: ElevenLabs voice ID to use.
        model_id: ElevenLabs model identifier.

    Returns:
        Path to the saved audio file.
    """
    result = generate_audio_preview(
        text=text,
        target_lang=target_lang,
        voice_id=voice_id,
        model_id=model_id,
    )

    with open(output_path, "wb") as f:
        f.write(result["audio_bytes"])

    return output_path


def list_available_voices() -> list:
    """
    List available ElevenLabs voices.

    Returns:
        List of voice information dictionaries.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")

    client = ElevenLabs(api_key=api_key)
    voices = client.voices.get_all()

    return [
        {
            "voice_id": v.voice_id,
            "name": v.name,
            "accent": getattr(v, "accent", ""),
            "gender": getattr(v, "gender", ""),
            "age": getattr(v, "age", ""),
            "use_case": getattr(v, "use_case", ""),
        }
        for v in voices.voices
    ]


if __name__ == "__main__":
    result = generate_audio_preview(
        text="Bienvenue dans notre application",
        target_lang="fr",
        model_id="eleven_multilingual_v2",
    )
    print(f"Generated {result['audio_size_bytes']} bytes of audio using model {result['model_id']}")
