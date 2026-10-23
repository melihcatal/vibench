import requests

from speech_client import assemblyai_headers, get_env


def submit_transcription(audio_url: str = ""):
    base_url = get_env("ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com")
    if not audio_url:
        audio_url = get_env("AUDIO_URL")
    response = requests.post(
        f"{base_url}/v2/transcript",
        headers=assemblyai_headers(),
        json={"audio_url": audio_url, "speaker_labels": False},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
