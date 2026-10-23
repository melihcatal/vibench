import os
import base64
from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient
from translation_models import TranslationResponse


DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_MODEL = "eleven_multilingual_v2"


def generate_audio_preview(
    translations: list[TranslationResponse],
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    output_format: str = "mp3_44100_128",
) -> dict:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable is required for ElevenLabs TTS API access"
        )

    client = ElevenLabs(api_key=api_key)

    audio_results = []

    for translation in translations:
        for result in translation.results:
            text = result.text

            audio_stream = client.text_to_speech.convert(
                voice_id=voice_id,
                output_format=output_format,
                text=text,
                model_id=model,
            )

            audio_bytes = b"".join(chunk for chunk in audio_stream)
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

            audio_results.append(
                {
                    "text": text,
                    "source_lang": translation.source_lang,
                    "target_lang": translation.target_lang,
                    "voice_id": voice_id,
                    "model": model,
                    "format": output_format,
                    "audio_base64": audio_base64,
                    "audio_size_bytes": len(audio_bytes),
                }
            )

    return {
        "audio_previews": audio_results,
        "total_generated": len(audio_results),
        "voice_id": voice_id,
        "model": model,
        "service": "ElevenLabs Text to Speech",
    }


def list_available_voices() -> list[dict]:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable is required for ElevenLabs TTS API access"
        )

    client = ElevenLabs(api_key=api_key)
    voices = client.voices.get_all()

    return [
        {
            "voice_id": voice.voice_id,
            "name": voice.name,
            "category": voice.category,
            "language": voice.labels.get("language", "en") if voice.labels else "en",
        }
        for voice in voices.voices
    ]
