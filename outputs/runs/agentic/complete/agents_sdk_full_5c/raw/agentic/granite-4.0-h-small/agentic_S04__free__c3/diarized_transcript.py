import os
import json
import requests
from speech_client import get_batch_client

# Configurable environment variables for Azure Cognitive Services Speech Service
# Required: AZURE_SPEECH_BATCH_KEY, AZURE_SPEECH_BATCH_REGION

def request_diarized_transcription(audio_path, speaker_count=2):
    """Requests a batch transcription with speaker diarization.

    Returns a tuple (job_id, location_header) for status polling.
    """
    client = get_batch_client()
    url = f"{client.endpoint}/speech/v1.0/transcriptions"
    payload = {
        "files": [audio_path],
        "properties": {
            "WordLevelTimestamps": "False",
            "SpeakerDiarization": "True",
            "SpeakerCount": str(speaker_count)
        }
    }
    headers = {
        "Ocp-Apim-Subscription-Key": client.sub_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    job_id = data.get("id")
    location = response.headers.get("Location")
    return job_id, location

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python diarized_transcript.py <audio.wav> [speaker_count=2]\n")
        sys.exit(1)
    audio = sys.argv[1]
    speakers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    job_id, location = request_diarized_transcription(audio, speakers)
    print(f"Diarized job submitted (ID: {job_id}, Location: {location})")
