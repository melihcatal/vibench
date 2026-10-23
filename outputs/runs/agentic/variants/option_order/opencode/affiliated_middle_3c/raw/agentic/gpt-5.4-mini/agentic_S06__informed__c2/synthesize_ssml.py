import requests

from speech_client import load_config, build_headers
from speech_models import ssml_wrap


def synthesize_ssml(
    ssml: str,
    voice_id: str | None = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> bytes:
    cfg = load_config()
    voice = voice_id or cfg.voice or "default"
    response = requests.post(
        f"{cfg.base_url}/text-to-speech/{voice}",
        headers=build_headers(cfg.api_key),
        json={
            "text": ssml_wrap(ssml),
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
            },
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.content
