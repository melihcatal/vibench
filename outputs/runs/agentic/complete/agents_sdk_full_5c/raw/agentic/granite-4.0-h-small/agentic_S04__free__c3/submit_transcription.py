import os
import requests
from speech_client import get_batch_client
from speech_models import BatchTranscriptionRequest

# Configurable environment variables for Azure Cognitive Services Speech Service
# Required: AZURE_SPEECH_BATCH_KEY, AZURE_SPEECH_BATCH_REGION

def submit_transcription(audio_paths):
    """Submits a list of audio file paths for batch transcription.

    Returns a tuple (job_id, location_header) for later polling.
    """
    client = get_batch_client()
    url = f"{client.endpoint}/speech/v1.0/transcriptions"
    payload = {"files": audio_paths}
    headers = {
        "Ocp-Apim-Subscription-Key": client.sub_key,
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    job_id = data.get("id")
    location = response.headers.get("Location")
    return job_id, location

if __name__ == "__main__":
    # Example usage: pass one or more .wav files
    import sys
    if len(sys.argv) < 2:
        print("Usage: python submit_transcription.py <audio1.wav> [audio2.wav ...]")
        sys.exit(1)
    files = sys.argv[1:]
    job_id, location = submit_transcription(files)
    print(f"Submitted batch job ID: {job_id} - Location header: {location}")
