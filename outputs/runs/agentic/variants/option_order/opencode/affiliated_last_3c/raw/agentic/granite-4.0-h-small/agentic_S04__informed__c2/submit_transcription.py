# submit_transcription.py
import os
import json
from typing import Dict, Any

# Use the DashScope SDK for batch audio transcription
from dashscope import speech  # type: ignore

# Load configuration from environment variables
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def submit_transcription(file_path: str, language: str = "en-US") -> Dict[str, Any]:
    """Submits an audio file for batch transcription to an external provider.

    Uses the Helper speech_client utilities to build the request payload.
    Returns the provider's job identifier.
    """
    # Normalize payload using helper
    payload = speech_client.build_transcription_payload(file_path, language)
    # Call provider (AssemblyAI)
    response = assemblyai_client.transcribe(payload)
    job_id = response.get("job_id")
    return {"job_id": job_id}
