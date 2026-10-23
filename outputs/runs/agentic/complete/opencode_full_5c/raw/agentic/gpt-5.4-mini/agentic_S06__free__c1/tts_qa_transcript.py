import os
import requests

OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def transcribe_sample(audio_path: str) -> str:
    with open(audio_path, "rb") as f:
        r = requests.post(OPENAI_TRANSCRIBE_URL, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}, files={"file": f}, data={"model": "whisper-1"})
    r.raise_for_status()
    return r.json()["text"]
