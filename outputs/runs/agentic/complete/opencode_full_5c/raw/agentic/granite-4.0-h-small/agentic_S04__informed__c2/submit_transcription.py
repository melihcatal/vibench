import os
import json
from assemblyai import AssemblyAI

# Load API key from environment
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Initialize AssemblyAI client
aai = AssemblyAI(ASSEMBLYAI_API_KEY)


def submit_transcription(audio_path: str) -> str:
    """Submit an audio file for batch transcription using AssemblyAI.
    Returns the upload URL or job ID for later polling.
    """
    request = {
        "audio_url": audio_path,
        "config": {"speaker_diarization": False, "timestamps": "words"},
    }
    response = aai.transcript.upload(request)
    return response["id"]
