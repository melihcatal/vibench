import requests


def transcribe_tts_sample(audio_url: str, api_key: str) -> dict:
    response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers={"authorization": api_key, "content-type": "application/json"},
        json={"audio_url": audio_url},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
