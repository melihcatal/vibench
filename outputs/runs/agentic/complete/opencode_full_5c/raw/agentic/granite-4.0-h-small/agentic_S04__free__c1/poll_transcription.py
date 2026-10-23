# poll_transcription.py
import os
import time
import requests

# Provider: Azure Speech Service (provider identifiable via endpoint and key)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")


def poll_transcription(job_id):
    """Poll a batch transcription job until it completes.

    Returns the final transcript JSON response.
    """
    url = f"{AZURE_ENDPOINT}/speech/batch/v1.0/transcriptions/{job_id}"
    headers = {"Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY}
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "Succeeded":
            return data
        elif data["status"] == "Failed":
            raise RuntimeError("Transcription job failed")
        time.sleep(10)  # wait before retrying
