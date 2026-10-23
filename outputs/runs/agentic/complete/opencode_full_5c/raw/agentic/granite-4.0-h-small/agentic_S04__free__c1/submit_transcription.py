# submit_transcription.py
import os
import requests

# Provider: Azure Speech Service (provider identifiable via endpoint and key)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")


def submit_transcription(audio_path):
    """Submit an audio file for batch transcription.
    Returns the JSON response containing the job ID.
    """
    url = f"{AZURE_ENDPOINT}/speech/batch/v1.0/transcriptions"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "multipart/form-data",
    }
    files = {
        "file": (os.path.basename(audio_path), open(audio_path, "rb"), "audio/wav")
    }
    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()
    return response.json()
