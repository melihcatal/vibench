import os

import requests


def transcribe_audio(audio_bytes: bytes):
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    headers = {"authorization": api_key}
    upload = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=audio_bytes,
        timeout=60,
    ).json()
    transcript = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers={**headers, "content-type": "application/json"},
        json={"audio_url": upload["upload_url"]},
        timeout=30,
    ).json()
    return transcript
