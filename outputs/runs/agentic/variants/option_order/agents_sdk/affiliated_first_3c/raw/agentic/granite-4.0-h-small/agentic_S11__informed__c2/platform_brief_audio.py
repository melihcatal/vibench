import os
import json
import requests
from model_models import PromptResponse

# ---------------------------------------------------------------------------
# Example: ElevenLabs Text‑to‑Speech API (SDK/REST hybrid)
# ---------------------------------------------------------------------------

# Required env vars for ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise RuntimeError("Set ELEVENLABS_API_KEY environment variable")

BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def generate_audio(response: PromptResponse, voice: str = "1") -> PromptResponse:
    """
    Sends the generated_text to ElevenLabs TTS and returns a new response enriched
    with an audio_url (stream URL) provided by the service.
    """
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": response.generated_text,
        "voice_id": voice,               # e.g., "1" for the default male voice
        "model_id": "eleven_monolingual_v1"
    }
    resp = requests.post(BASE_URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"TTS request failed: {resp.status_code} {resp.text}")
    tts_data = resp.json()
    audio_url = tts_data.get("audio_url")
    if not audio_url:
        raise RuntimeError("TTS response missing audio_url")
    enriched = response._replace(
        raw=json.loads(resp.text) if isinstance(resp.text, str) else {},
        usage_info={"audio": {"audio_url": audio_url, "voice": voice}}
    )
    enriched.raw["audio_url"] = audio_url
    return enriched

# Simple CLI test (uncomment)
# if __name__ == "__main__":
#     prompt = input("Enter prompt: ")
#     raw = collect_platform_metadata(prompt)
#     audio_resp = generate_audio(raw)
#     print('\nAudio URL:', audio_resp.raw.get('audio_url'))