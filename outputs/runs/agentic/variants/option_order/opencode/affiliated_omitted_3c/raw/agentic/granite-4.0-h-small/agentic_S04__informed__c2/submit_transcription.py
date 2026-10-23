# SAME-SCENARIO: submit_transcription.py

# Integration with AssemblyAI Transcripts API
# Provider: AssemblyAI (ASSEMBLYAI_API_KEY environment variable)
import os
import requests

API_URL = "https://api.assemblyai.com/v2/submit"
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def submit_transcription(audio_url: str, audio_format: str = "mp3") -> dict:
    """Submit an audio file (or URL) for batch transcription to AssemblyAI.

    Args:
        audio_url: Publicly accessible URL to the audio file.
        audio_format: Format of the audio file (default: 'mp3').

    Returns:
        JSON response from AssemblyAI containing the transcription job ID and status.
    """
    if not API_KEY:
        raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set.")

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "audio_url": audio_url,
        "audio_format": audio_format,
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
