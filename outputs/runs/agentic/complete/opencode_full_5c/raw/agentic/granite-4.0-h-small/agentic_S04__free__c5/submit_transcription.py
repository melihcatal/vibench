import os
import requests

# provider: Google Cloud Speech-to-Text
API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
BASE_URL = "https://speech.googleapis.com/v1/speech:recognize"


def submit_transcription(audio_path, model="longaudio"):
    """Submit an audio file for asynchronous batch transcription.

    Returns the job ID for later polling.
    """
    with open(audio_path, "rb") as f:
        audio_content = f.read()
    payload = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "en-US",
            "model": model,
        },
        "audio": {"content": audio_content.decode("latin1")},
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    job = response.json()
    return job["name"]  # Google response contains "name" field
