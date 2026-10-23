import requests
from model_client import get_elevenlabs_api_key
from model_models import TTSRequest, TTSResponse


def generate_spoken_brief(request: TTSRequest) -> TTSResponse:
    api_key = get_elevenlabs_api_key()
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is not set.")

    voice_id = request.voice_id or "21m00Tcm4TlvDq8ikWAM"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }

    data = {
        "text": request.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    return TTSResponse(audio_content=response.content, raw_response=response)
