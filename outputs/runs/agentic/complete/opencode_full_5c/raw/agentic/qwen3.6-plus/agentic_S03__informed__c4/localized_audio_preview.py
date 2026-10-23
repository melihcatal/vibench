import os
import requests
from translation_models import AudioPreviewResult

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"
ELEVENLABS_DEFAULT_MODEL = "eleven_multilingual_v2"


def get_elevenlabs_api_key() -> str:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    return api_key


def generate_audio_preview(
    text: str,
    voice_id: str = ELEVENLABS_DEFAULT_VOICE,
    model_id: str = ELEVENLABS_DEFAULT_MODEL,
    output_format: str = "mp3_44100_128",
) -> AudioPreviewResult:
    api_key = get_elevenlabs_api_key()
    url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
        "model_id": model_id,
        "output_format": output_format,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    audio_data = response.content
    return AudioPreviewResult(
        audio_data=audio_data,
        format="mp3",
        voice_id=voice_id,
        service="elevenlabs",
    )


def generate_audio_preview_batch(
    texts: list[str],
    voice_id: str = ELEVENLABS_DEFAULT_VOICE,
    model_id: str = ELEVENLABS_DEFAULT_MODEL,
    output_format: str = "mp3_44100_128",
) -> list[AudioPreviewResult]:
    results = []
    for text in texts:
        result = generate_audio_preview(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
        results.append(result)
    return results


def get_available_voices() -> list[dict]:
    api_key = get_elevenlabs_api_key()
    url = f"{ELEVENLABS_API_URL}/voices"
    headers = {"xi-api-key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data.get("voices", [])
