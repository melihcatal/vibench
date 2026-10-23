import os
import requests

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
BASE_URL = "https://api.assemblyai.com/v2"


def get_assemblyai_client():
    if not ASSEMBLYAI_API_KEY:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")

    headers = {"authorization": ASSEMBLYAI_API_KEY, "content-type": "application/json"}

    session = requests.Session()
    session.headers.update(headers)
    return session


def post_transcript(audio_url, options=None):
    client = get_assemblyai_client()
    payload = {"audio_url": audio_url}
    if options:
        payload.update(options)

    response = client.post(f"{BASE_URL}/transcript", json=payload)
    response.raise_for_status()
    return response.json()


def get_transcript(transcript_id):
    client = get_assemblyai_client()
    response = client.get(f"{BASE_URL}/transcript/{transcript_id}")
    response.raise_for_status()
    return response.json()
