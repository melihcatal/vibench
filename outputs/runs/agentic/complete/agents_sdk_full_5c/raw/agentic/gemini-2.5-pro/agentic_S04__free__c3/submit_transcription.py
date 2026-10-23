import os
import requests
import time
from speech_client import get_assemblyai_session

def submit_transcription_job(audio_url: str) -> str:
    """Submits a new transcription job to AssemblyAI."""
    session = get_assemblyai_session()
    url = "https://api.assemblyai.com/v2/transcript"
    
    payload = {
        "audio_url": audio_url
    }
    
    response = session.post(url, json=payload)
    response.raise_for_status()
    
    job_id = response.json()["id"]
    return job_id
