import os
import httpx
from speech_models import normalize_ssml_request


def synthesize_ssml(
    ssml: str,
    model: str = "tts-1-hd",
    voice: str = "nova",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> bytes:
    api_key = os.environ.get("OPENAI_API_KEY")
    payload = normalize_ssml_request(ssml, model, voice, response_format, speed)
    with httpx.Client(base_url="https://api.openai.com/v1") as client:
        response = client.post(
            "/audio/speech",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60.0,
        )
        response.raise_for_status()
    return response.content
