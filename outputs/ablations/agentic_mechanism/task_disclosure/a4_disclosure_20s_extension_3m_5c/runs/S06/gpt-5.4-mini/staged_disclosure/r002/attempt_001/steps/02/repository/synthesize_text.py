import os
import urllib.parse
import urllib.request


def synthesize_text(text: str) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{urllib.parse.quote(voice_id)}"
    payload = (
        '{"text": ' + __import__("json").dumps(text) + ', "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}}'
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()
