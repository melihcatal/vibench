import os
import requests
from speech_client import get_elevenlabs_api_key
from speech_models import TTSRequest, TTSResponse


ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"
DEFAULT_SSML_MODEL = "eleven_multilingual_v2"


def synthesize_ssml(
    ssml: str,
    voice_id: str = None,
    model_id: str = DEFAULT_SSML_MODEL,
    output_format: str = "mp3_44100_128",
) -> TTSResponse:
    api_key = get_elevenlabs_api_key()
    if voice_id is None:
        voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")

    url = f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}/stream"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": ssml,
        "model_id": model_id,
        "output_format": output_format,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)
    response.raise_for_status()

    audio_bytes = b"".join(response.iter_content(chunk_size=8192))

    return TTSResponse(
        audio_data=audio_bytes,
        voice_id=voice_id,
        model_id=model_id,
        format=output_format,
        provider="elevenlabs",
    )
