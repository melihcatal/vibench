import json
import os
from typing import Dict, Any

# Assume the service uses Azure Cognitive Services Batch Speech-to-Text
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, AudioDataStream, SpeechSynthesizer

# Load endpoint and key from environment (these should be set in your runtime environment)
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SERVICE_REGION = os.getenv("AZURE_SPEECH_REGION")

def poll_transcription(job_id: str) -> Dict[str, Any]:
    """Poll the status of a submitted batch transcription job.

    Returns the JSON response from the service, including 'state' and 'results'.
    """
    import requests
    url = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speech/batch/v1/jobs/{job_id}"
    headers = {"Authorization": f"Bearer {SPEECH_KEY}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Export the poll helper for later-step usage
__all__ = ["poll_transcription"]
