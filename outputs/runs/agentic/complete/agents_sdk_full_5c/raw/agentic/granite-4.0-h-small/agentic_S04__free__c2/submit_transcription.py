import json
import os
from typing import Dict, Any

# Assume the service uses Azure Cognitive Services Batch Speech-to-Text
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, AudioDataStream, SpeechSynthesizer

# Load endpoint and key from environment (these should be set in your runtime environment)
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SERVICE_REGION = os.getenv("AZURE_SPEECH_REGION")

def submit_transcription(audio_path: str, callback_url: str = None, **kwargs) -> Dict[str, Any]:
    """Submit a batch transcription request to Azure Cognitive Services.

    Returns the JSON response containing the job ID.
    """
    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
    # The Batch Speech-to-Text endpoint requires a SAS URL for the audio file blob storage.
    # Here we assume the caller provides a valid SAS URL.
    params = {
        "contentUrls": [audio_path],
        "properties": {
            "diarization": kwargs.get("diarization", False),
            "timestamps": kwargs.get("timestamps", True),
            "callbackUrl": callback_url,
        },
    }
    # Use the REST API for batch jobs (POST https://{region}.api.cognitive.microsoft.com/speech/batch/v1)
    import requests
    url = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speech/batch/v1"
    headers = {
        "Authorization": f"Bearer {SPEECH_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=params, headers=headers)
    response.raise_for_status()
    return response.json()

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

# Helper to extract the transcript text once the job is completed.
def extract_transcript(response_json: Dict[str, Any]) -> str:
    if response_json.get("state") != "Succeeded":
        raise ValueError("Job not yet completed")
    results = response_json.get("results")
    transcripts = [r.get("Transcript") for r in results if r.get("Transcript")]
    return "\n".join(transcripts)

# Export only the helpers needed by downstream steps
__all__ = ["submit_transcription", "poll_transcription", "extract_transcript"]
