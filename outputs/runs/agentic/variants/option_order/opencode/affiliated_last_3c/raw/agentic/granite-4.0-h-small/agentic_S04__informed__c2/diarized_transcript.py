# diarized_transcript.py
import os
from typing import Dict, Any

# Use DashScope SDK to request speaker diarization for a recorded meeting
from dashscope import speech  # type: ignore

# Load configuration from environment variables
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def diarized_transcript(file_path: str, num_speakers: int = 2) -> Dict[str, Any]:
    """Requests speaker diarization for a recording and returns the diarized transcript.

    Uses the Helper speech_client to construct the diarization request.
    """
    # Build diarization request using helper utilities
    payload = speech_client.build_diarization_payload(file_path, num_speakers)
    response = assemblyai_client.diarize(payload)
    # Normalize the response into a consistent structure
    diarized = speech_client.normalize_diarized_response(response)
    return diarized
