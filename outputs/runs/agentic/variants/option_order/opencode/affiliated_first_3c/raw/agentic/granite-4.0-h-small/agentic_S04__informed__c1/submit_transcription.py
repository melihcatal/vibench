# SAME-SCENARIO implementation - submits an audio file for batch transcription using IBM Watson Speech to Text

import os
import json
from speech_client import get_stt_client

# Identifier for the provider
PROVIDER = "IBM Watson Speech to Text"


def submit_transcription(file_path, language="en-US"):
    """Submits an audio file for batch transcription.

    Args:
        file_path (str): Path to the audio file.
        language (str): Language code for transcription (default 'en-US').

    Returns:
        dict: Response containing job ID and status.
    """
    client = get_stt_client()
    # Submit batch transcription request (sync mode for demo)
    response = client.recognize(
        audio=open(file_path, "rb"),
        content_type="audio/wav",
        model=f"{language}_BroadbandModel",
        diarization=True,
        timestamps=True,
        results_per_page=100,
    )
    # Return a simplified dict with job identifier
    return {
        "job_id": response.get("result_id"),
        "status": "submitted",
        "provider": PROVIDER,
        "language": language,
    }
